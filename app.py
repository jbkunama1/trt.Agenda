import os, json, sqlite3, secrets, re
from pathlib import Path
from flask import Flask, request, jsonify, render_template
app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=100_000
DB=os.environ.get('DATABASE','/data/agenda.sqlite3')
PASSWORD=os.environ.get('EDIT_PASSWORD','')
THEMES=('ocean','graphite','paper','forest','sunset')
if not PASSWORD:
    raise RuntimeError('EDIT_PASSWORD muss gesetzt sein.')
Path(DB).parent.mkdir(parents=True,exist_ok=True)
def connect():
    con=sqlite3.connect(DB,timeout=10)
    try:
        con.execute('BEGIN IMMEDIATE')
        con.execute('CREATE TABLE IF NOT EXISTS agendas (id INTEGER PRIMARY KEY CHECK(id BETWEEN 1 AND 5), body TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 0)')
        if con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='agenda'").fetchone():
            old=con.execute('SELECT body,version FROM agenda WHERE id=1').fetchone()
            if old:
                data=json.loads(old[0]);data.setdefault('theme','ocean')
                con.execute('INSERT OR IGNORE INTO agendas VALUES (1,?,?)',(json.dumps(data),old[1]))
        for ident in range(1,6):
            items=[{'title':t,'minutes':m} for t,m in [('Ankommen',5),('Einstieg',10),('Arbeitsphase',8),('Austausch',12),('Abschluss',5)]] if ident==1 else []
            data={'title':'Unsere Agenda' if ident==1 else f'Agenda {ident}','start':'08:00','theme':'ocean','items':items}
            con.execute('INSERT OR IGNORE INTO agendas VALUES (?,?,0)',(ident,json.dumps(data)))
        con.commit()
        return con
    except Exception:
        con.rollback();con.close();raise

def ident():
    raw=request.args.get('agenda','1')
    if raw not in ('1','2','3','4','5'):
        raise ValueError()
    return int(raw)

def read(con,number):
    body,version=con.execute('SELECT body,version FROM agendas WHERE id=?',(number,)).fetchone()
    return {'id':number,'data':json.loads(body),'version':version}

@app.get('/')
def index():
    return render_template('index.html')
@app.get('/api/agendas')
def list_agendas():
    con=connect()
    try:
        return jsonify(agendas=[{'id':n,'title':json.loads(b)['title']} for n,b in con.execute('SELECT id,body FROM agendas ORDER BY id')])
    finally:
        con.close()
@app.get('/api/agenda')
def get_agenda():
    try:
        number=ident()
    except ValueError:
        return jsonify(error='Agenda muss 1 bis 5 sein.'),400
    con=connect()
    try:
        return jsonify(read(con,number))
    finally:
        con.close()

def validate(payload):
    if not isinstance(payload,dict):raise ValueError()
    data=payload.get('data');version=payload.get('version')
    if not isinstance(data,dict) or type(version) is not int or version<0:raise ValueError()
    title,start,items=data.get('title'),data.get('start'),data.get('items')
    theme=data.get('theme','ocean')
    if not isinstance(title,str) or not 1<=len(title.strip())<=120:raise ValueError()
    if not isinstance(start,str) or not re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d',start):raise ValueError()
    if not isinstance(theme,str) or theme not in THEMES:raise ValueError()
    if not isinstance(items,list) or len(items)>50:raise ValueError()
    clean=[]
    for item in items:
        if not isinstance(item,dict):raise ValueError()
        t,m=item.get('title'),item.get('minutes')
        if not isinstance(t,str) or not 1<=len(t.strip())<=160 or type(m) is not int or not 1<=m<=1440:raise ValueError()
        clean.append({'title':t.strip(),'minutes':m})
    return {'title':title.strip(),'start':start,'theme':theme,'items':clean},version
@app.put('/api/agenda')
def save_agenda():
    if not secrets.compare_digest(request.headers.get('X-Edit-Key','').encode(),PASSWORD.encode()):
        return jsonify(error='Bearbeitungsschlüssel ist falsch.'),401
    try:
        number=ident();clean,version=validate(request.get_json(silent=True))
    except ValueError:
        return jsonify(error='Agenda, Titel, Startzeit, Theme und Dauer prüfen.'),400
    con=connect()
    try:
        cur=con.execute('UPDATE agendas SET body=?,version=version+1 WHERE id=? AND version=?',(json.dumps(clean),number,version))
        con.commit()
        if not cur.rowcount:return jsonify(error='Diese Agenda wurde inzwischen geändert. Änderungen kopieren, abbrechen und neu laden.'),409
        return jsonify(version=version+1)
    finally:
        con.close()
@app.get('/health')
def health():
    return jsonify(status='ok')
@app.after_request
def headers(response):
    response.headers['Cache-Control']='no-store'
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors "+os.environ.get('FRAME_ANCESTORS','*')
    return response
