#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('./vocal.db')
cursor = conn.cursor()

print "Opened database successfully";

conn.execute("INSERT INTO Users (username, password, name, age,location,description) \
      VALUES ('paul', 'password', 'Paul', '15', 'California', 'desc test' )");

conn.execute("INSERT INTO Users (username, password, name, age,location,description) \
      VALUES ('johnny13', 'password', 'John', '14', 'California', 'desc test' )");

print "test entry entered";

cursor.execute("""
select * from Users U
""")
for row in cursor:
    print row

conn.commit()
conn.close()