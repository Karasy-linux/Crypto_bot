import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from sqlite3 import Error
from loguru import logger 

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException

import service
from service import COINS_STR


# loggig
logger.add(
    "logs/bot.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="00:00", 
    retention="2 days"
)


load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.critical("TOKEN is invalid")
    os._exit()
    
bot = AsyncTeleBot(TOKEN)