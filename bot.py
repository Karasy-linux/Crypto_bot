# Copyright (C) 2026 Karasy-linux
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from sqlite3 import Error
from loguru import logger 

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException

import get_data
from get_data import supported_coins




#CASHING
load_dotenv()
TOKEN = os.getenv("TOKEN")



bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def cmd_start(message: Message) -> None:
    user_name = message.from_user.username
    chat_id = message.chat.id

    text = ( 
        f"Hello, @{user_name or "user"}" 
        "\nthis bot for" 
        " to monitoring "
        "\ncoins" \
        " Commands: " \
        "\n/subscribe"
        "\n/price" 
        "\n/unsubscribe"\
            )
    

    await bot.reply_to(message=message, text=text)
    try:
        await get_data.add_user_info(chat_id, user_name if user_name else "user")

    except Error as e:
        logger.warning(f"Error of the database {e}")
    except ApiTelegramException as e:
        logger.error("Telegram API error {e}")



#_______________________________________________________________________________
#_______________________________________________________________________________
#_____________________________THE SUBSCRIBE LOGIC_______________________________
#_______________________________________________________________________________




@bot.message_handler(commands=['subscribe'])
async def cmd_subscribe(message: Message) -> None:

    parts = message.text.split()
    
    if len(parts) < 2:
        await bot.reply_to(
            message, 
            "Usage: /subscribe &lt;coin_name&gt;\nExample: <code>/subscribe bitcoin</code>",
            parse_mode='HTML')
        return

    coin = parts[1].lower() 

    if coin not in supported_coins:
        bot.reply_to(message, f"I don't track {coin}. Try: {', '.join(supported_coins)}")
        return

    # save to base
    await get_data.subscribe(message.chat.id, coin)
    
    await bot.reply_to(message, f"✅ Done! Now monitoring {coin.capitalize()}.")
   



@bot.message_handler(commands=['unsubscribe'])
async def cmd_subscribe(message: Message) -> None:

    parts = message.text.split()
    
    if len(parts) < 2:
        bot.reply_to(
            message, 
            "Usage: /unsubscribe &lt;coin_name&gt;\nExample: <code>/unsubscribe bitcoin</code>",
            parse_mode='HTML')
        return

    coin = parts[1].lower() 

    if coin not in supported_coins:
        bot.reply_to(message, f"I don't track {coin}. Try: {', '.join(supported_coins)}")
        return

    # save to base
    await get_data.unsubscribe(message.chat.id, coin)
    
    await bot.reply_to(message, f"✅ Done! Now unmonitoring {coin.capitalize()}.")
   



@bot.message_handler(commands=['change_percent'])
async def cmd_change(message:Message) -> None:
    parts = message.text.split()

    if len(parts) < 3:
        await bot.reply_to(
            message, 
            "Usage: /change_percent &ltcoin_name&gt;\nExample: <code>/change_percent bitcoin 0.**</code> - your percent",
            parse_mode='HTML')
        return
    try:
        coin = parts[1].lower()
        percent = float(parts[2])
        chat_id = message.chat.id
        

        await get_data.change_percent(percent,coin,chat_id)
        text = f"✅ Done! You changed the percent for <b>{coin}</b> to <b>{percent}</b>"

        await bot.reply_to(message,text=text,parse_mode='HTML')

        logger.info(f"User {chat_id} updated {coin} to {percent}%")
    except Exception as e:
        logger.error(f"change is failed \n {e}")
        bot.reply_to(message,f"{parts[1].lower()} is invalid")
  



@bot.message_handler(commands=['price'])
async def cmd_view(message:Message) -> None:
    parts = message.text.split()
    
    if len(parts) < 2:
        bot.reply_to(
            message, 
            "Usage: /price &ltcoin_name&gt;\nExample: <code>/price bitcoin</code>",
            parse_mode='HTML')
        return
    
    coin = parts[1]
    if coin not in supported_coins:
        await bot.reply_to(message, f"I don't track {coin}. Try: {', '.join(supported_coins)}")
        return
    
    for c, p in get_data.view(): #[('bitcoin', 81964.0), ('ethereum', 2339.34), ('solana', 97.76)] 
        if c == coin:
            price = p
    await bot.reply_to(message, f"price {coin}: {price}" )        




async def price_monitor():
    while True:
        try:
            prices = get_data.get_fresh_price()

            for chat_id, asset_id, percent, last_price in get_data.get_data_subcribers():
                coin = get_data.translate_asset_id(asset_id)
                price = prices.get(coin,{}).get('usd',0)

                if last_price == 0:
                    get_data.add_price(asset_id, chat_id, price)
                    continue    

                current_percent = (price - last_price) / last_price
                if abs(current_percent) >= percent:
    
                    await bot.send_message(chat_id, f"🚨 {coin} changed!")
                    get_data.add_price(asset_id, chat_id, price)
        except Error as e:
            logger.error(f"no price change was made: {e}")

        await asyncio.sleep(500)    




@bot.message_handler(commands=['button'])
def cmd_button_message(message: Message) -> None:
    # Create the keyboard
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Create the button VALUES (?, ?)", coins)

    item1 = KeyboardButton("/start")
    item2 = KeyboardButton("/crypto_sub")
    
    
    markup.add(item1)
    markup.add(item2)

    bot.send_message(
        chat_id=message.chat.id, 
        text='Choose what you need', 
        reply_markup=markup
    )




@bot.message_handler(commands=['code'])
def view_code(message:Message) -> None:
    text =("""
            this bot is open source project\\. Link to GitHub:\n
            [Crypto\\_sender](https://github.com/Karasy-linux/Crypto_bot)
            """)
    bot.reply_to(message=message,
                 text=text,
                 parse_mode="MarkdownV2",
                 disable_web_page_preview=True)



async def main():
    logger.success("launch the bot")

    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())
     
