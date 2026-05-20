import sqlite3

from service import QUERIES
from service import SUPPORTED_COINS


def init(db='data.db') -> None:
    with sqlite3.connect(db) as con:
        query = QUERIES.get("tables","")
        cur = con.cursor()
        cur.executescript(query) 

        con.commit()


def assets(db='data.db') -> None:
    with sqlite3.connect(db) as con:
        query = "INSERT OR IGNORE INTO assets (coin_name) VALUES (?)"
        cur = con.cursor()
        for coin in SUPPORTED_COINS:
            cur.execute(query,(coin,))    

        con.commit()


init()
assets()
