#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('./files/vocal.db')
cursor = conn.cursor()

print "Opened database successfully";

# conn.execute("INSERT INTO Users (username, password, name, age,location,description) \
#       VALUES ('paul', 'password', 'Paul', '15', 'California', 'desc test' )");

# conn.execute("INSERT INTO Users (username, password, name, age,location,description) \
#       VALUES ('johnny13', 'password', 'John', '14', 'California', 'desc test' )");

# conn.execute("INSERT INTO User_likes (liker, likee, like_type) \
#       VALUES ('Paul', 'Ryan', 'true')");

# conn.execute("INSERT INTO User_likes (liker, likee, like_type) \
#       VALUES ('Ryan', 'Paul', 'false')");

# conn.execute("INSERT INTO User_likes (liker, likee, like_type) \
#       VALUES ('Paul', 'Beth', 'true')");

# conn.execute("INSERT INTO User_likes (liker, likee, like_type) \
#       VALUES ('Beth', 'Paul', 'true')");

# conn.execute("INSERT INTO User_likes (liker, likee, like_type) \
#       VALUES ('Paul', 'Sarah', 'true')");

# conn.execute("INSERT INTO User_likes (liker, likee, like_type) \
#       VALUES ('Sarah', 'Paul', 'true')");

print "likes";

cursor.execute("""
select * from User_likes U
""")
for row in cursor:
    print row

print "Users";

cursor.execute("""
select * from Users U
""")
for row in cursor:
    print row



conn.commit()
conn.close()