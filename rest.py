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

def get_save_path_for_category(category):
    base = "./files/sounds/"
    save_path = os.path.join (base, category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path


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

@app.get('/Users/<username>')
def showUser(id, db):
    cursor = db.execute('select * from Users where id=?', [id])
    row = cursor.fetchone()
    if not row:
        return bottle.HTTPError(404, "User not found")

    return {
        'id': row['id'],
        'username': row['username'],
        'name': row['name'],
        'description': row['description']
    }

@app.get('/Users/exists/<username>')
def isUser(username, db):
    cursor = db.execute('select * from Users where username=?', [username])
    row = cursor.fetchone()
    if not row:
        return {
            'exists': "false"
        }

    return {
        'exists': "true"
    }

@app.post('/Users')
def createUser(db):
    data = bottle.request.forms
    cursor = db.execute('insert into Users (username, password) values (?, ?)',
        (data['username'], data['password']))
    return {
            'success': "true"
        }
    #return { "link": make_url('Users', cursor.lastrowid) }

@app.post('/Login')
def createUser(db):
    data = bottle.request.forms
    new_data = (data['username'], data['password'])
    cursor = db.execute('select * from Users where username=? AND password=?', new_data)
    row = cursor.fetchone()
    if not row:
        return {
            'success': "false"
        }

    return {
        'success': "true"
    }

#upload file named 'upload' with category and username information included
@app.post('/upload')
def do_upload():
    username = request.forms.get('username')
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.wav','.mp3'):
        return 'File extension not allowed.'

    save_path = get_save_path_for_category(category)
    filename = username + ext
    file_path = os.path.join(savepath, filename)
    upload.save(file_path)
    return 'OK'

if 'REQUEST_METHOD' in os.environ :
    app.run(server='cgi')
else:
    app.run(host='localhost', port=8000, debug=True, reloader=True)
