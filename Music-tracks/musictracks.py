import xml.etree.ElementTree as ET
import sqlite3

connection = sqlite3.connect('Mtrackdb.sqlite')
cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS Artist')
cur.execute('DROP TABLE IF EXISTS Genre')
cur.execute('DROP TABLE IF EXISTS Album')
cur.execute('DROP TABLE IF EXISTS Track')

# fresh table formation
cur.execute('CREATE TABLE Artist (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name  TEXT UNIQUE)')

cur.execute('CREATE TABLE Genre (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE)')

cur.execute('CREATE TABLE Album (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT UNIQUE, artist_id  INTEGER)')

cur.execute('CREATE TABLE Track (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT UNIQUE, album_id INTEGER, genre_id INTEGER, len INTEGER, rating INTEGER, count INTEGER)')

filename = input('enter xml file: ')
if (len(filename) < 1): filename = 'Library.xml'

# looking up for key-value pair in xml file.
def search(root, key):
    found = False
    for child in root:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

# parsing of xml file
stuff = ET.parse(filename)
lst = stuff.findall('dict/dict/dict')
print('Dict count: ', len(lst))

# searching for Various data of table.
for data in lst:
    if ( search(data, 'Track ID') is None ): continue
    name = search(data, 'Name')
    artist = search(data, 'Artist')
    genre = search(data, 'Genre')
    album = search(data, 'Album')
    count = search(data, 'Play Count')
    rating = search(data, 'Rating')
    length = search(data, 'Total Time')

    if name is None or artist is None or album is None: continue

    print(name, artist, album, count, rating, length)

    # inserting, and fetching of value in table
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES(?)', (artist, ))
    cur.execute('SELECT id FROM Artist WHERE name = ?', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES(?)', (genre, ))
    cur.execute('SELECT id FROM Genre WHERE name = ?', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES(?, ?)', (album, artist_id))
    cur.execute('SELECT id FROM Album WHERE title = ?', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES(?, ?, ?, ?, ?, ?)', (name, album_id, genre_id, length, rating, count))

    connection.commit()
