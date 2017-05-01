#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('./files/vocal.db')
print "Opened database successfully";

#conn.execute('DROP TABLE IF EXISTS "USER_LIKES"')
conn.execute('''CREATE TABLE USER_LIKES
       (LIKER		CHAR(50) PRIMARY KEY NOT NULL,
       LIKEE				CHAR(50),
       LIKE_TYPE           BOOLEAN,
       FOREIGN KEY(LIKEE) REFERENCES USERS(USERNAME),
       FOREIGN KEY(LIKER) REFERENCES USERS(USERNAME));''')
print "Table created successfully";

conn.close()
