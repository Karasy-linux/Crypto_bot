import sqlite3

from loguru import logger
import requests
from config import API_KEY



#__________________________________________________________________________________________
#__________________________________________________________________________________________
#____________________________THE CASHING___________________________________________________
#__________________________________________________________________________________________




SQL_FILES = {
            "monitoring":"sql/monitoring.sql",
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




#__________________________________________________________________________________________
#__________________________________________________________________________________________
#________________________THE DATABASE LOGIC________________________________________________
#__________________________________________________________________________________________




def translate_coin(coin:str,db = 'data.db' ) -> int:
    with sqlite3.connect(db) as con:
        try:
            query = "SELECT id FROM assets WHERE name = (?);"

            cur = con.cursor()
            cur.execute(query,(coin,))
            asset_id = cur.fetchone()

            return asset_id[0] if asset_id else 0
        except sqlite3.Error as e:
            logger.error(f"Error of the database: {e}")




def add_price(coin:str, new_price:float, db='data.db' ) -> None:
    asset_id = translate_coin(coin)
    if asset_id is None:
        logger.error(f"Not founded {coin}")
        return 
    try:
        con = sqlite3.connect(db)
        with con:
            cur = con.cursor()
            query = "INSERT INTO history (price,asset_id) VALUES (?,?);"

            cur.execute(query,(new_price,asset_id))
    except sqlite3.Error as e:
        logger.error(f"Error of the database \n {e}")




def add_user_info(chat_id:int, user_name:str, db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:
            cur = con.cursor()
            query = "INSERT INTO users(chat_id,user_name) VALUES(?,?);"
            cur.execute(query,(chat_id,user_name,))

            # Оце — логування рівня Senior розробника:
            logger.success(f"User @{user_name or 'unknown'} (ID: {chat_id}) was successfully added to the database")
            con.commit()
        except sqlite3.Error as e:
            logger.error(f"User @{user_name or 'unknown'} (ID: {chat_id}) was UNSUCCESSFULLY added to the database")


#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#____________________________THE USER LOGIC___________________________________________________
#_____________________________________________________________________________________________



def view(db='data.db') -> dict:
    with sqlite3.connect(db) as con:
        try:
            query = QUERIES.get("view",None)
            if not query:
                logger.error(f"view is not founded")
                return
            cur = con.cursor()
            cur.execute(query)    
            res = cur.fetchall()

            return res if res else None
        except sqlite3.Error as e:
            logger.error(f"error the database \n {e}")




def subscribe(chat_id:int, coin:str, db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:    
            query = QUERIES.get("subscribe",None)
            if query is None:
                return
            
            asset_id = translate_coin(coin)
            cur = cur.execute(query)
            cur.execute(query,(chat_id,coin,asset_id))

            logger.success(f"User (chat_id):{chat_id} subscribed to {coin}") 
            con.commit()  
        except sqlite3.Error as e:
            logger.error(f"Error of the database: \n{e}")



def unsubscribe(chat_id:int, coin:str, db='data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        try:    
            query = QUERIES.get("unsubscribe",None)
            if query is None:
                return 
            asset_id = translate_coin(coin)
            cur = con.cursor()
            cur.execute(query,(chat_id,coin,asset_id))    
            
            logger.success(f"User (chat_id):{chat_id} unsubscribed to {coin}") 
            con.commit()  
        except sqlite3.Error as e:
            logger.error(f"Error of the database: \n{e}")



def change_percent(percent:float, coin:str, chat_id:int,db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:
            query = """
                    UPDATE subscribers
                    SET percent = ?
                    WHERE chat_id = ? AND coin = ?;
                    """
            cur = con.cursor()
            cur.execute(query,(percent,chat_id,coin))

            if cur.rowcount == 0:
                logger.warning(f"Subscription not found: User {chat_id}, coin {coin}")
                raise Exception("Subscription not found")
            con.commit()
            logger.success(f"Update: User {chat_id}, coin {coin} -> {percent}%")

        except sqlite3.Error as e:
            logger.error(f"Error of the database: {e}")
            raise




def get_alerts(db='data.db') -> dict:
    try:
        with sqlite3.connect(db) as con:
            query = QUERIES.get("monitoring")

            cur = con.cursor()
            cur.execute(query)

            alerts = cur.fetchall()
            logger.success(f"Users get alart")
            return alerts 

    except sqlite3.Error as e:
        logger.error(f"Error of the database {e}")
        




#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#_______________________THE UPDATE DATA LOGIC_________________________________________________
#_____________________________________________________________________________________________#




session = requests.Session()
session.headers.update({
    "Bot": "@crypto_sender385_bot"
})


def update_data(endpoint="https://api.coingecko.com/api/v3/simple/price") -> None:
    """
    This function fetches the prices from CoinGecko 
    to add to the database
    """
    params ={
        "ids": 'bitcoin,ethereum,solana',
        "vs_currencies": 'usd'
    }
    try:
        headers = {
            "x-cg-demo-api-key": API_KEY
            }
        response = session.get(endpoint,params=params,headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        for coin in data.keys():
            price = data.get(coin,{}).get('usd',0)
            add_price(coin,price)

            print(f"Record: {coin} -> {price}")
                  

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e.response.status_code}")
    except sqlite3.Error as e:
        logger.error(f"beda: {e}")    
    except Exception as e:
        logger.error(f"Full beda: {e}")
    


