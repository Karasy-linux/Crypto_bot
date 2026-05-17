import sqlite3
import os
from dotenv import load_dotenv
from get_data import QUERIES



load_dotenv()
COINS = os.getenv("COINS")

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