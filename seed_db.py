import sqlite3
from config import COINS




def init_db(sql_file = 'sql/tables.sql', db = 'data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        with open(sql_file, "r") as f:
            query = f.read()
        try:
            cur.executescript(query)
        except sqlite3.Error as e:
            print(e)
    


def seed_db(db = 'data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        query = "INSERT OR IGNORE INTO assets (id, name) VALUES (?, ?)"
        cur.executemany(query,(COINS))    


init_db()
seed_db()        