import sqlite3

from loguru import logger
import requests
from config import API_KEY


#__________________________________________________________________________________________
#__________________________________________________________________________________________
#________________________________THE DATABASE LOGIC________________________________________
#__________________________________________________________________________________________




def translate_coin(coin:str,db = 'data.db' ) -> int:
    con = sqlite3.connect(db)
    with con:
        try:
            cur = con.cursor()
            query = "SELECT id FROM assets WHERE name = (?);"

            cur.execute(query,(coin,))
            asset_id = cur.fetchone()

            return asset_id[0] if asset_id else 0
        except sqlite3.Error as e:
            print(f"beda: {e}")




def add_price(coin:str, new_price:float, db='data.db' ) -> None:
    asset_id = translate_coin(coin)
    if asset_id is None:
        print(f"Error {coin}")
        return 
    try:
        con = sqlite3.connect(db)
        with con:
            cur = con.cursor()
            query = "INSERT INTO history (price,asset_id) VALUES (?,?);"

            cur.execute(query,(new_price,asset_id))
    except sqlite3.Error as e:
        print(f"beda {e}")



def add_user_info(chat_id:int, user_name:str,sql_file='sql/user_info.sql', db='data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        with open(sql_file, "r") as f:
            query = f.read()
        cur.execute(query,(chat_id,user_name,))




#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#______________________________________THE USER LOGIC_________________________________________
#_____________________________________________________________________________________________



def view(sql_file='sql/view.sql',db='data.db') -> dict:
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        with open(sql_file,"r") as f:
            query = f.read()
        cur.execute(query)    
        res = cur.fetchall()
        return res if res else None





def subscribe(chat_id:int, coin:str, sql_file='sql/subscribe.sql', db='data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        with open(sql_file, "r") as f:
            query = f.read()
        asset_id = translate_coin(coin)
        cur.execute(query,(chat_id,coin,asset_id))    




def unsubscribe(chat_id:int, coin:str, sql_file='sql/unsubscribe.sql', db='data.db') -> None:
    con = sqlite3.connect(db)
    with con:
        cur = con.cursor()
        with open(sql_file, "r") as f:
            query = f.read()
        asset_id = translate_coin(coin)
        cur.execute(query,(chat_id,coin,asset_id))    




def change_percent(percent:float, coin:str, chat_id:int,sql_file='sql/change_percent.sql',db='data.db') -> None:
    with sqlite3.connect(db) as con:
        try:
            with open(sql_file,"r") as f:
                query = f.read()
            cur = con.cursor()
            cur.execute(query,(percent,chat_id,coin))

            if cur.rowcount == 0:
                logger.warning(f"Subscription not found: User {chat_id}, coin {coin}")
                raise Exception("Subscription not found")
            con.commit()
            logger.success(f"Оновлено: User {chat_id}, coin {coin} -> {percent}%")

        except sqlite3.Error as e:
            logger.error(f"Error of the database: {e}")
            raise

def get_alerts(sql_file='sql/monitoring.sql',db='data.db') -> dict:
    with sqlite3.connect(db) as con:
        with open(sql_file,"r") as f:
            query = f.read()
        cur = con.cursor()
        cur.execute(query)

        alerts = cur.fetchall()
        return alerts 
        




#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
#_________________________________THE UPDATE DATA LOGIC_______________________________________
#_____________________________________________________________________________________________#




session = requests.Session()
session.headers.update({
    "Bot": "@crypto_sender385_bot"
})


def update_data(endpoint="https://api.coingecko.com/api/v3/simple/price") -> None:
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

            print(f"Записую: {coin} -> {price}")
                  

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
    except sqlite3.Error as e:
        print(f"beda: {e}")    
    except Exception as e:
        print(f"Full beda: {e}")
    


