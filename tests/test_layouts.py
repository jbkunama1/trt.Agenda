import importlib.util
from pathlib import Path
import pytest

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('EDIT_PASSWORD','test-secret')
    monkeypatch.setenv('DATABASE',str(tmp_path/'agenda.sqlite3'))
    spec=importlib.util.spec_from_file_location('agenda_layouts',Path(__file__).parents[1]/'app.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.app.config['TESTING']=True
    return module.app.test_client()

H={'X-Edit-Key':'test-secret'}

def test_defaults(client):
    data=client.get('/api/agenda').json['data']
    assert data['layout']=='list' and data['theme']=='ocean'
    assert all('emoji' not in i for i in data['items'])

@pytest.mark.parametrize('theme',['ocean','graphite','paper','forest','sunset','70s','80s','90s','modern','cyberpunk','neon','terminal','pastell'])
@pytest.mark.parametrize('layout',['list','columns','timeline','tiles'])
def test_theme_layout_combinations(client,theme,layout):
    p=client.get('/api/agenda?agenda=2').json
    p['data'].update(theme=theme,layout=layout,items=[{'title':'Start','minutes':5,'emoji':'🚀'},{'title':'Ohne','minutes':3,'emoji':'  '}])
    assert client.put('/api/agenda?agenda=2',json=p,headers=H).status_code==200
    saved=client.get('/api/agenda?agenda=2').json['data']
    assert saved['theme']==theme and saved['layout']==layout
    assert saved['items'][0]['emoji']=='🚀' and 'emoji' not in saved['items'][1]

def test_old_payload_without_layout(client):
    p=client.get('/api/agenda').json;del p['data']['layout']
    assert client.put('/api/agenda',json=p,headers=H).status_code==200
    assert client.get('/api/agenda').json['data']['layout']=='list'

@pytest.mark.parametrize('field,value',[('layout','grid'),('layout',3),('theme','unknown')])
def test_invalid_values(client,field,value):
    p=client.get('/api/agenda').json;p['data'][field]=value
    assert client.put('/api/agenda',json=p,headers=H).status_code==400

@pytest.mark.parametrize('emoji',['x'*17,5,'a\nb'])
def test_invalid_emoji(client,emoji):
    p=client.get('/api/agenda').json;p['data']['items'][0]['emoji']=emoji
    assert client.put('/api/agenda',json=p,headers=H).status_code==400

@pytest.mark.parametrize('path',['/static/layouts.css','/static/themes-extra.css','/static/copy.js','/static/view.html'])
def test_static_files(client,path):
    assert client.get(path).status_code==200

def test_index_has_copy_buttons(client):
    html=client.get('/').get_data(as_text=True)
    assert 'id="copy-link"' in html and 'id="copy-iframe"' in html and 'layout-select' in html
