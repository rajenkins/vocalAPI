#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('vocal.db')
print "Opened database successfully";

conn.execute('DROP TABLE IF EXISTS "USERS"')
conn.execute('''CREATE TABLE USERS
       (ID INTEGER PRIMARY KEY,
       NAME           CHAR(50)    NOT NULL,
       PHOTO            CHAR(50)     NOT NULL,
       LOCATION        CHAR(50),
       DESCRIPTION         CHAR(50));''')
print "Table created successfully";

conn.close()
