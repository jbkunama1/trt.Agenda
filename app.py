import os, json, sqlite3, secrets, re
from pathlib import Path
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100_000
DB = os.environ.get('DATABASE', '/data/agenda.sqlite3')
PASSWORD = os.environ.get('EDIT_PASSWORD', '')
if not PASSWORD:
    raise RuntimeError('EDIT_PASSWORD muss gesetzt sein.')
Path(DB).parent.mkdir(parents=True, exist_ok=True)
def connect():
    con = sqlite3.connect(DB, timeout=10)
    con.execute('CREATE TABLE IF NOT EXISTS agenda (id INTEGER PRIMARY KEY CHECK(id=1), body TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 0)')
    initial = {'title':'Unsere Agenda','start':'08:00','items':[{'title':t,'minutes':m} for t,m in [('Ankommen',5),('Einstieg',10),('Arbeitsphase',8),('Austausch',12),('Abschluss',5)]]}
    con.execute('INSERT OR IGNORE INTO agenda VALUES (1, ?, 0)', (json.dumps(initial),))
    con.commit()
    return con
@app.get('/')
def index():
    return render_template('index.html')
@app.get('/api/agenda')
def get_agenda():
    con = connect()
    try:
        body, version = con.execute('SELECT body, version FROM agenda WHERE id=1').fetchone()
        return jsonify(data=json.loads(body), version=version)
    finally:
        con.close()
def validate(payload):
    if not isinstance(payload, dict):
        raise ValueError()
    data = payload.get('data')
    version = payload.get('version')
    if not isinstance(data, dict) or type(version) is not int or version < 0:
        raise ValueError()
    title, start, items = data.get('title'), data.get('start'), data.get('items')
    if not isinstance(title,str) or not 1 <= len(title.strip()) <= 120:
        raise ValueError()
    if not isinstance(start,str) or not re.fullmatch(r'([01]\d|2[0-3]):[0-5]\d', start):
        raise ValueError()
    if not isinstance(items,list) or len(items) > 50:
        raise ValueError()
    clean = []
    for item in items:
        if not isinstance(item,dict):
            raise ValueError()
        t, m = item.get('title'), item.get('minutes')
        if not isinstance(t,str) or not 1 <= len(t.strip()) <= 160 or type(m) is not int or not 1 <= m <= 1440:
            raise ValueError()
        clean.append({'title':t.strip(),'minutes':m})
    return {'title':title.strip(),'start':start,'items':clean}, version
@app.put('/api/agenda')
def save_agenda():
    key = request.headers.get('X-Edit-Key','')
    if not secrets.compare_digest(key.encode('utf-8'), PASSWORD.encode('utf-8')):
        return jsonify(error='Bearbeitungsschlüssel ist falsch.'), 401
    try:
        clean, version = validate(request.get_json(silent=True))
    except ValueError:
        return jsonify(error='Bitte Titel, Startzeit und Dauer (1–1440 Minuten) prüfen.'),400
    con=connect()
    try:
        cur=con.execute('UPDATE agenda SET body=?, version=version+1 WHERE id=1 AND version=?',(json.dumps(clean),version))
        con.commit()
        if not cur.rowcount:
            return jsonify(error='Die Agenda wurde inzwischen geändert. Bitte Änderungen kopieren und neu laden.'),409
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
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors " + os.environ.get('FRAME_ANCESTORS','*')
    return response
