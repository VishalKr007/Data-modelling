import json
import sqlite3

# connecting to database datadb
connection = sqlite3.connect('datadb.sqlite')
cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS User')
cur.execute('DROP TABLE IF EXISTS Course')
cur.execute('DROP TABLE IF EXISTS Member')

# Formation of database table
cur.execute('CREATE TABLE User(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE )')
cur.execute('CREATE TABLE Course(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT UNIQUE)')
cur.execute('CREATE TABLE Member(user_id INTEGER, course_id INTEGER, role INTEGER, PRIMARY KEY (user_id, course_id))')

#input of json file
record = input('enter filename: ')
if (len(record) < 1): record = 'roster_data_sample.json'

# parsing of json file
data = open(record).read()
info = json.loads(data)
print('data count: ', len(info))

for i in info:
    Name = i[0];
    Title = i[1];
    Role = i[2]

    print(Name, Title, Role)

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES( ? )', (Name, ) )
    cur.execute('SELECT id FROM User WHERE name = ?', (Name, ))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES(?)', (Title, ))
    cur.execute('SELECT id FROM Course WHERE title = ?', (Title, ))
    course_id = cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Member (user_id, course_id) VALUES(?, ?)', (user_id, course_id))

    connection.commit()
