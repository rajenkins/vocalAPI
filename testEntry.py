#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('./vocal.db')
cursor = conn.cursor()

print "Opened database successfully";

conn.execute("INSERT INTO Users (name,photo,location,description) \
      VALUES ('Paul', 'abc123', 'California', 'desc test' )");

conn.execute("INSERT INTO Users (name,photo,location,description) \
      VALUES ('John', 'abc124', 'Cali', 'test desc' )");

print "test entry entered";

cursor.execute("""
select * from Users U
""")
for row in cursor:
    print row

conn.commit()
conn.close()