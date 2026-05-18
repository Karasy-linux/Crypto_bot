import sqlite3
import os
from dotenv import load_dotenv

from loguru import logger
import requests



#__________________________________________________________________________________________
#__________________________________________________________________________________________
#____________________________THE CASHING___________________________________________________
#__________________________________________________________________________________________




load_dotenv()
API_KEY = os.getenv("API_KEY")

SQL_FILES = {
            "tables":"sql/tables.sql",
            "view":"sql/view.sql",
            "subscribe":"sql/subscribe.sql",
            "unsubscribe":"sql/unsubscribe.sql"
            }

QUERIES = {}

for query_name, path_name in SQL_FILES.items():
    try:
        with open(path_name,"r",encoding='UTF-8') as f:
            QUERIES[query_name] = f.read()
    except FileNotFoundError as e:
        logger.critical(f"Critical error: {e}")
        QUERIES[query_name] = ""


SUPPORTED_COINS = 'bitcoin,ethereum,solana'
supported_coins = SUPPORTED_COINS.split(',')

COINS = [
        (1, 'bitcoin'),
        (2, 'ethereum'),
        (3, 'solana'),
        ]




#__________________________________________________________________________________________
#__________________________________________________________________________________________
#________________________THE DATABASE LOGIC________________________________________________
#__________________________________________________________________________________________




def update_price(asset_id:int, chat_id:int, new_price:float, db='data.db' ) -> None:
    coin = translate_asset_id(asset_id)
    if asset_id is None:
        logger.error(f"Not founded {asset_id}")
        return 
    with sqlite3.connect(db) as con:
        try:
            query = """
                    UPDATE subscribers 
                    SET last_price 
                    WHERE asset_id = ? AND chat_id = ?;
                    """

            cur = con.cursor()
            cur.execute(query,(new_price,asset_id))
            
            con.commit()
            logger.success(f"The price of {coin} was successfully added to the database")
        except sqlite3.Error as e:
            logger.error(f"Error of the database \n {e}")




def add_user_info(chat_id:int, user_name:str, db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:
            cur = con.cursor()
            query = "INSERT INTO users(chat_id,user_name) VALUES(?,?);"
            cur.execute(query,(chat_id,user_name,))

            logger.success(f"User @{user_name or 'unknown'} (ID: {chat_id}) was successfully added to the database")
            con.commit()
        except sqlite3.Error as e:
            logger.warning(f"User @{user_name or 'unknown'} (ID: {chat_id}) was UNSUCCESSFULLY added to the database")




#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#____________________________THE GETS DATA____________________________________________________
#_____________________________________________________________________________________________




def translate_asset_id(asset_id:int,db = 'data.db' ) -> int:
    with sqlite3.connect(db) as con:
        try:
            query = "SELECT name FROM assets WHERE id = (?);"

            cur = con.cursor()
            cur.execute(query,(asset_id,))
            asset_id = cur.fetchone()

            return asset_id[0] if asset_id else 0
        except sqlite3.Error as e:
            logger.error(f"Error of the database: {e}")




def get_data_subcribers(db='data.db'):
    with sqlite3.connect(db) as con:
        try:
            query = "SELECT chat_id, asset_id, percent, last_price FROM subscribers;"
            cur = con.cursor()
            cur.execute(query)

            for chat_id, asset_id, percent, last_price in cur.fetchall():
                yield chat_id, asset_id, percent, last_price
        except sqlite3.Error as e:
            logger.error(f"fetch is failed {e}")    




session = requests.Session()
session.headers.update({
    "Bot": "@crypto_sender385_bot"
})


def get_fresh_price(endpoint="https://api.coingecko.com/api/v3/simple/price") -> dict:
    params ={
        "ids": SUPPORTED_COINS,
        "vs_currencies": 'usd'
    }
    try:
        headers = {
            "x-cg-demo-api-key": API_KEY
            }
        response = session.get(endpoint,params=params,headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e.response.status_code}") 
    except Exception as e:
        logger.error(f"Full beda: {e}")




#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#____________________________THE USER LOGIC___________________________________________________
#_____________________________________________________________________________________________




def view(chat_id:int,asset_id:int,db='data.db') -> dict:
    with sqlite3.connect(db) as con:
        try:
            query = QUERIES.get("view",None)
            if not query:
                logger.error(f"view is not founded")
                return
            cur = con.cursor()
            cur.execute(query,(chat_id,asset_id))    
            res = cur.fetchall()

            return res if res else None
        except sqlite3.Error as e:
            logger.error(f"error the database \n {e}")




def subscribe(chat_id:int, asset_id:int, db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:    
            query = QUERIES.get("subscribe",None)
            if query is None:
                return
            
            coin = translate_asset_id(asset_id)
            cur = con.cursor()
            cur.execute(query,(chat_id,asset_id))

            logger.success(f"User (chat_id):{chat_id} subscribed to {coin}") 
            con.commit()  
        except sqlite3.Error as e:
            logger.error(f"Error of the database: \n{e}")




def unsubscribe(chat_id:int, asset_id:int, db='data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        try:    
            query = QUERIES.get("unsubscribe",None)
            if query is None:
                return 
            coin = translate_asset_id(asset_id)
            cur = con.cursor()
            cur.execute(query,(chat_id,asset_id))    
            
            logger.success(f"User (chat_id):{chat_id} unsubscribed to {coin}") 
            con.commit()  
        except sqlite3.Error as e:
            logger.error(f"Error of the database: \n{e}")




def change_percent(percent:float, asset_id:int, chat_id:int,db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:
            query = """
                    UPDATE subscribers
                    SET percent = ?
                    WHERE chat_id = ? AND asset_id = ?;
                    """
            cur = con.cursor()
            cur.execute(query,(percent,chat_id,asset_id))

            if cur.rowcount == 0:
                logger.warning(f"Subscription not found: User {chat_id}, asset_id {asset_id}")
                raise Exception("Subscription not found")
            con.commit()
            logger.success(f"Update: User {chat_id}, asset_id {asset_id} -> {percent}%")

        except sqlite3.Error as e:
            logger.error(f"Error of the database: {e}")
            raise




#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#_______________________THE UPDATE DATA LOGIC_________________________________________________
#_____________________________________________________________________________________________#

