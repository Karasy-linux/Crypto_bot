import sqlite3
from config import COINS




def init_db(sql_file = 'sql/tables.sql', db = 'data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        with open(sql_file, "r") as f:
            query = f.read()
        cur.executescript(query)
        try:
            cur.execute("""
                ALTER TABLE subscribers 
                ADD COLUMN percent REAL DEFAULT 0.1;
                """)
        except sqlite3.Error as e:
            print(f"beda: {e}")
        cur.execute("CREATE INDEX idx_history_coin_time ON history(asset_id, timestamp);")



def seed_db(db = 'data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        query = "INSERT OR IGNORE INTO assets (id, name) VALUES (?, ?)"
        cur.executemany(query,(COINS))    


init_db()
seed_db()        