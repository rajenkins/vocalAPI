#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('./files/vocal.db')
print "Opened database successfully";

conn.execute('DROP TABLE IF EXISTS "SOUNDFILES"')
conn.execute('''CREATE TABLE SOUNDFILES
       (USERNAME		CHAR(50) PRIMARY KEY NOT NULL,
       CAT1				CHAR(50),
       CAT2           CHAR(50),
       CAT3				CHAR(50),
       CAT4           CHAR(50),
       FOREIGN KEY(USERNAME) REFERENCES USERS(USERNAME));''')
print "Table created successfully";

conn.close()
