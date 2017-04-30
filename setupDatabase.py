#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('vocal.db')
print "Opened database successfully";

conn.execute('DROP TABLE IF EXISTS "USERS"')
conn.execute('''CREATE TABLE USERS
       (ID INTEGER PRIMARY KEY,
       USERNAME			CHAR(50) NOT NULL,
       PASSWORD			CHAR(50) NOT NULL,
       NAME           CHAR(50),
       AGE				CHAR(50),
       LOCATION        CHAR(50),
       DESCRIPTION         CHAR(50));''')
print "Table created successfully";

conn.close()
