#!/usr/bin/python
import bottle
import bottle.ext.sqlite
import os
from bottle import route, request, static_file, run
import requests
from pydub import AudioSegment
#AudioSegment.converter = "/afs/cs.unc.edu/project/courses/comp580-s17/public_html/users/Vocal/_ffmpeg"


app = bottle.Bottle()
plugin = bottle.ext.sqlite.Plugin(dbfile='./files/vocal.db')
app.install(plugin)

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def make_url(table, id):
    parts = bottle.request.urlparts
    path = parts[2].replace('/r1.cgi','')
    return '%s://%s%s/%s' % (parts[0], parts[1], path, id)

def get_sound_url(username, category):
    parts = bottle.request.urlparts
    path = parts[2].replace('/rest.cgi','/files')
    return '%s://%s%s.wav' % (parts[0], parts[1], path)

def get_sound_url_for_Users(username, category):
    parts = bottle.request.urlparts
    path = parts[2].replace('/rest.cgi/Users','/files/sounds/cat1')
    return '%s://%s%s.wav' % (parts[0], parts[1], path)

def does_url_exist(sound_url):
    response = requests.head(sound_url)
    return response.status_code < 400

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

# def convert_wav_to_mp3(save_path, username, full_file_path):
#     #AudioSegment.converter = "./ffmpeg-3.3"
#     wav_audio = AudioSegment.from_file(full_file_path, format="wav")
#     new_file_path = os.path.join(save_path, username + ".mp3")
#     if os.path.exists(new_file_path):
#         os.remove(new_file_path)
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     wav_audio.export(new_file_path, format="mp3")

def convert_m4a_to_wav(save_path, username, full_file_path):
    #AudioSegment.converter = "./ffmpeg-3.3"
    m4a_audio = AudioSegment.from_file(full_file_path, format="m4a")
    new_file_path = os.path.join(save_path, username + ".wav")
    if os.path.exists(new_file_path):
        os.remove(new_file_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    m4a_audio.export(new_file_path, format=".wav")



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
def showUser(username, db):
    cursor = db.execute('select * from Users where username=?', [username])
    row = cursor.fetchone()
    if not row:
        return bottle.HTTPError(404, "User not found")

    sound_url = get_sound_url_for_Users(username,'cat1')
    if does_url_exist(sound_url):
        return {
            'id': row['id'],
            'age': row['age'],
            'username': row['username'],
            'BioUrl': "http://wwwx.cs.unc.edu/Courses/comp580-s17/users/Vocal/files/sounds/cat2/Paul.wav",
            'name': row['name'],
            'description': row['description']
        }

    else:
        return {
            'id': row['id'],
            'age': row['age'],
            'username': row['username'],
            'BioUrl': "http://wwwx.cs.unc.edu/Courses/comp580-s17/users/Vocal/files/sounds/cat2/Paul.wav",
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

@app.get('/Users/matches/<username>')
def getMatches(username, db):
    cursor = db.execute('''SELECT  ul1.liker
                        FROM    user_likes ul1 
                        WHERE ul1.like_type = "true" AND ul1.likee = ?
                        AND ul1.liker 
                        IN
                        (
                        SELECT  ul2.likee
                        FROM    user_likes ul2
                        WHERE ul2.liker = ? AND ul2.like_type="true"
                        )''', (username, username))
    result = [ row['liker']
               for row in cursor ]
    return { 'data': result }

@app.get('/Users/queue/<username>')
def getMatches(username, db):
    cursor = db.execute('''SELECT  u.username
                            FROM    users u 
                            WHERE NOT u.username = ? AND u.username 
                            NOT IN
                                (
                                SELECT  ul.likee
                                FROM    user_likes ul
                                WHERE ul.liker = ?
                                )''', (username, username))
    result = [ row['username']
               for row in cursor ]
    return { 'data': result }

@app.get('/sounds/<category>/<username>')
def getUpload(username, category, db):
    sound_url = get_sound_url(username,'cat1')
    if does_url_exist(sound_url):
        return { "link": sound_url }
    else:
        return "Sound does not exist"

@app.post('/Users')
def createUser(db):
    data = bottle.request.forms
    cursor = db.execute('insert into Users (username, password, age) values (?, ?, ?)',
        (data['username'], data['password'], 0))
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
    if category not in ('cat1','cat2','cat3','cat4'):
        return 'Category does not exist.'
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.wav','.mp3', '.3gpp', '.m4a', '.mp4'):
        return 'File extension not allowed.'
    save_path = get_save_path_for_category(category)
    filename = username + ext
    file_path = os.path.join(save_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    upload.save(file_path)

    #convert saved file to mp3
    # if ext == '.wav':
    #     convert_wav_to_mp3(save_path, username, file_path)
    if ext == '.m4a':
        convert_m4a_to_wav(save_path, username, file_path)

    #delete the wav file
    # if os.path.exists(file_path):
    #     os.remove(file_path)


    return 'OK'

@app.post('/Users/update')
def createUser(db):
    data = bottle.request.forms
    if 'age' in data and 'name' in data:
        cursor = db.execute('UPDATE Users SET age = ?, name= ? WHERE username = ?;',
            (data['age'], data['name'], data['username']))
        return { 'updated_age': "true", 'updated_name': "true"}

    elif 'age' in data:
        cursor = db.execute('UPDATE Users SET age = ? WHERE username = ?;',
            (data['age'], data['username']))
        return { 'updated_age': "true", 'updated_name': "false"}

    elif 'name' in data:
        cursor = db.execute('UPDATE Users SET name = ? WHERE username = ?;',
            (data['name'], data['username']))
        return { 'updated_age': "false", 'updated_name': "true"}

    return { 'updated_age': "false", 'updated_name': "false"}

@app.post('/Users/like')
def createUser(db):
    data = bottle.request.forms
    cursor = db.execute('insert into User_likes (liker, likee, like_type) values (?, ?, ?)',
        (data['liker'], data['likee'], data['like_type']))
    if data['like_type']:
        return { 'liked': "true" }
    else:
        return { 'liked': "false" }


if 'REQUEST_METHOD' in os.environ :
    app.run(server='cgi')
else:
    app.run(host='localhost', port=8000, debug=True, reloader=True)
