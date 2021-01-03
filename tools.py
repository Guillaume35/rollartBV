import sqlite3
from pathlib import Path

# dict_factory()
# convert data to dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# getDb()
# get database connection
def getDb():
    home_path = str(Path.home())
    db_path = home_path + '/.rollartBV/structure.db'
    conn = sqlite3.connect(db_path)

    return conn