import sqlite3

from get_data import supported_coins
from get_data import QUERIES

def init_db(db = 'data.db') -> None:
    with sqlite3.connect(db) as con:
        query = QUERIES.get("tables")
        
        cur = con.cursor()
        cur.executescript(query)
        con.commit()




def seed_db(db = 'data.db') -> None:
    with sqlite3.connect(db) as con:
        query = "INSERT OR IGNORE INTO assets (name) VALUES (?)"

        cur = con.cursor()
        for coin in supported_coins:
            cur.execute(query,(coin,))    

        con.commit()

init_db()
seed_db()        