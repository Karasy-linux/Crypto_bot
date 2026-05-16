import sqlite3
from config import COINS
from get_data import QUERIES


def init_db(db = 'data.db') -> None:
    with sqlite3.connect(db) as con:
        query = QUERIES.get("tables")
        
        cur = con.cursor()
        cur.executescript(query)




def seed_db(db = 'data.db') -> None:
    with sqlite3.connect(db) as con:
        query = "INSERT OR IGNORE INTO assets (id, name) VALUES (?, ?)"

        cur = con.cursor()
        cur.executemany(query,(COINS))    


init_db()
seed_db()        