import importlib.util,json,sqlite3
from pathlib import Path
import pytest

def module(monkeypatch,path):
    monkeypatch.setenv('EDIT_PASSWORD','test-secret');monkeypatch.setenv('DATABASE',str(path))
    spec=importlib.util.spec_from_file_location('multi',Path(__file__).parents[1]/'app.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_migration_idempotent(monkeypatch,tmp_path):
    path=tmp_path/'old.db';body={'title':'Bestehender Unterricht','start':'09:12','items':[{'title':'Erhalten','minutes':8}]}
    with sqlite3.connect(path) as c:
        c.execute('CREATE TABLE agenda(id INTEGER PRIMARY KEY CHECK(id=1),body TEXT,version INTEGER)');c.execute('INSERT INTO agenda VALUES(1,?,7)',(json.dumps(body),))
    m=module(monkeypatch,path);client=m.app.test_client();p=client.get('/api/agenda').json
    assert p['data']['title']==body['title'] and p['data']['items']==body['items'] and p['version']==7 and p['data']['theme']=='ocean'
    p['data']['theme']='forest';assert client.put('/api/agenda',json=p,headers={'X-Edit-Key':'test-secret'}).status_code==200
    assert client.get('/api/agenda').json['data']['theme']=='forest'
    assert len(client.get('/api/agendas').json['agendas'])==5
    with sqlite3.connect(path) as c:assert c.execute('SELECT body FROM agenda').fetchone()[0]==json.dumps(body)

def test_independent_slots(monkeypatch,tmp_path):
    client=module(monkeypatch,tmp_path/'new.db').app.test_client();headers={'X-Edit-Key':'test-secret'}
    for ident,theme in enumerate(('ocean','graphite','paper','forest','sunset'),1):
        p=client.get(f'/api/agenda?agenda={ident}').json;p['data']['theme']=theme;p['data']['title']=f'Titel {ident}'
        assert client.put(f'/api/agenda?agenda={ident}',json=p,headers=headers).status_code==200
        assert client.put(f'/api/agenda?agenda={ident}',json=p,headers=headers).status_code==409
    for ident,theme in enumerate(('ocean','graphite','paper','forest','sunset'),1):
        p=client.get(f'/api/agenda?agenda={ident}').json;assert p['data']['theme']==theme and p['data']['title']==f'Titel {ident}'
    assert client.get('/api/agenda?agenda=6').status_code==400
    p=client.get('/api/agenda').json;p['data']['theme']='invalid'
    assert client.put('/api/agenda',json=p,headers=headers).status_code==400
    assert client.get('/static/view.html').status_code==200
