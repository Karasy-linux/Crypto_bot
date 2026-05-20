import aiosqlite
import asyncio
import os 
from dotenv import load_dotenv
from loguru import logger



load_dotenv()
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    logger.critical("API_KEY is invalid")
    os._exit()



SQL_FILES ={
    "tables": "sql/tables.sql"
}

QUERIES = {}
for query_name, path in SQL_FILES.items():
    try:
        with open(path, "r") as f:
            QUERIES[query_name] = f.read()
    except FileNotFoundError as e:
        logger.critical(f"NOT FOUND {e}")
        QUERIES[query_name] = ""


COINS_API_STRING = "bitcoin,ethereum,solana"
SUPPORTED_COINS = tuple(COINS_API_STRING.split(","))




async def add_user_info(username:str,chat_id:int, db="data.db") -> None:
    async with aiosqlite.connect(db) as con:
        try:
            async with con.cursor() as cur:
                query = "INSERT OR IGNORE INTO users(username, chat_id) VALUES(?,?)"
                await cur.execute(query,(username,chat_id))
                await con.commit()
                logger.info(f"successfully added @{username} to the database")
        except aiosqlite.Error as e:
            logger.error("e")




async def change_laungage(chat_id:int, db='data.db') -> None:
    async with aiosqlite.connect(db) as con:
        try:
            async with con.cursor() as cur:
                query = "UPDATE users SET language = ? WHERE chat_id = ?"
                await cur.execute(query,(chat_id,))
                await con.commit()
                logger.info(f"successfully changed language")
        except aiosqlite.Error as e:
            logger.error()