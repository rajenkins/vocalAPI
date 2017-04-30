#!/usr/bin/python
import bottle
import bottle.ext.sqlite
import os
from bottle import route, request, static_file, run

app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile='./files/vocal.db')
app.install(plugin)

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def make_url(table, id):
    parts = bottle.request.urlparts
    path = parts[2].replace('/r1.cgi','')
    return '%s://%s%s/%s' % (parts[0], parts[1], path, id)

def query_to_where(sql, queryMap):
    query = bottle.request.query
    where = []
    args = []
    for key in query.keys():
        if key in queryMap:
            where.append('%s?' % queryMap[key])
            args.append(query[key])
    if where:
        return (sql + ' where ' + ' and '.join(where), args)
    else:
        return (sql, [])

@app.get('/Users')
def listUsers(db):
    queryMap = {
        'name' : 'name=',
        'photo' : 'photo=',
        'location' : 'location=',
        'description' : 'description=',
    }

    sql = 'select id, name from Users'
    sql, args = query_to_where(sql, queryMap)

    cursor = db.execute(sql, args)

    result = [ { 'link': make_url('Users', row['id']), 'name': row['name'] }
               for row in cursor ]

    # result = [ { 'id': row['id'], 'name': row['name'] }
    #            for row in cursor ]

    return { 'result': result }

@app.get('/Users/<id>')
def showUser(id, db):
    cursor = db.execute('select * from Users where id=?', [id])
    row = cursor.fetchone()
    if not row:
        return bottle.HTTPError(404, "Sailor not found")

    return {
        'id': row['id'],
        'name': row['name'],
        'description': row['description']
    }

@app.get('/Users/exist/<name>')
def isUser(name, db):
    cursor = db.execute('select * from Users where name=?', [name])
    row = cursor.fetchone()
    if not row:
        return {
            'exists': "false",
        }

    return {
        'exists': "true",
    }

@app.post('/Users')
def createUser(db):
    data = bottle.request.forms
    cursor = db.execute('insert into Users (name, photo, location, description) values (?, ?, ?, ?)',
        (data['name'], data['photo'], data['location'], data['description']))
    return { "link": make_url('Users', cursor.lastrowid) }

@app.post('/upload')
def do_upload():
    #category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    #if ext not in ('.png','.jpg','.jpeg'):
    #    return 'File extension not allowed.'

    #save_path = get_save_path_for_category(category)
    save_path = "./files/sounds/"
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'

if 'REQUEST_METHOD' in os.environ :
    app.run(server='cgi')
else:
    app.run(host='localhost', port=8000, debug=True, reloader=True)
