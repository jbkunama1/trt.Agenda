import importlib.util
from pathlib import Path
import pytest

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('EDIT_PASSWORD','test-secret')
    monkeypatch.setenv('DATABASE',str(tmp_path/'agenda.sqlite3'))
    spec=importlib.util.spec_from_file_location('agenda_test',Path(__file__).parents[1]/'app.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.config['TESTING']=True
    return module.app.test_client()

def test_read_and_page(client):
    assert client.get('/').status_code==200
    assert client.get('/health').json=={'status':'ok'}
    assert len(client.get('/api/agenda').json['data']['items'])==5

def test_auth_persistence_and_conflict(client):
    payload=client.get('/api/agenda').json
    assert client.put('/api/agenda',json=payload).status_code==401
    payload['data']['items'][0]['minutes']=12
    headers={'X-Edit-Key':'test-secret'}
    assert client.put('/api/agenda',json=payload,headers=headers).status_code==200
    assert client.get('/api/agenda').json['data']['items'][0]['minutes']==12
    assert client.put('/api/agenda',json=payload,headers=headers).status_code==409

@pytest.mark.parametrize('body',[None,[],{}, {'data':None,'version':0}, {'data':{'title':'A','start':'99:99','items':[]},'version':0}, {'data':{'title':'A','start':'08:00','items':[{'title':'A','minutes':0}]},'version':0}])
def test_validation(client,body):
    response=client.put('/api/agenda',json=body,headers={'X-Edit-Key':'test-secret'})
    assert response.status_code==400

def test_iframe_headers(client):
    response=client.get('/?embed=1')
    assert 'frame-ancestors *' in response.headers['Content-Security-Policy']
    assert 'X-Frame-Options' not in response.headers
