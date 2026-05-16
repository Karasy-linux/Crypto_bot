# Copyright (C) 2026 Karasy-linux
# SPDX-License-Identifier: GPL-3.0-or-later

import time
import threading
from sqlite3 import Error
from loguru import logger 

import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiTelegramException

from config import TOKEN
import get_data

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def cmd_start(message: Message) -> None:
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
    

    bot.reply_to(message=message, text=text)
    try:
        get_data.add_user_info(chat_id, user_name if user_name else "user")

    except Error as e:
        logger.error(f"Error of the database {e}")




#_______________________________________________________________________________
#_______________________________________________________________________________
#_____________________________THE SUBSCRIBE LOGIC_______________________________
#_______________________________________________________________________________




SUPPORTED_COINS = ['bitcoin','ethereum','solana']
@bot.message_handler(commands=['subscribe'])
def cmd_subscribe(message: Message) -> None:

    parts = message.text.split()
    
    if len(parts) < 2:
        bot.reply_to(
            message, 
            "Usage: /subscribe &lt;coin_name&gt;\nExample: <code>/subscribe bitcoin</code>",
            parse_mode='HTML')
        return

    coin = parts[1].lower() 

    if coin not in SUPPORTED_COINS:
        bot.reply_to(message, f"I don't track {coin}. Try: {', '.join(SUPPORTED_COINS)}")
        return

    # save to base
    get_data.subscribe(message.chat.id, coin)
    
    bot.reply_to(message, f"✅ Done! Now monitoring {coin.capitalize()}.")
   



@bot.message_handler(commands=['unsubscribe'])
def cmd_subscribe(message: Message) -> None:

    parts = message.text.split()
    
    if len(parts) < 2:
        bot.reply_to(
            message, 
            "Usage: /unsubscribe &lt;coin_name&gt;\nExample: <code>/unsubscribe bitcoin</code>",
            parse_mode='HTML')
        return

    coin = parts[1].lower() 

    if coin not in SUPPORTED_COINS:
        bot.reply_to(message, f"I don't track {coin}. Try: {', '.join(SUPPORTED_COINS)}")
        return

    # save to base
    get_data.unsubscribe(message.chat.id, coin)
    
    bot.reply_to(message, f"✅ Done! Now unmonitoring {coin.capitalize()}.")
   



@bot.message_handler(commands=['change_percent'])
def cmd_change(message:Message) -> None:
    parts = message.text.split()

    if len(parts) < 3:
        bot.reply_to(
            message, 
            "Usage: /change_percent &ltcoin_name&gt;\nExample: <code>/change_percent bitcoin 0.**</code> - your percent",
            parse_mode='HTML')
        return
    try:
        coin = parts[1].lower()
        percent = float(parts[2])
        chat_id = message.chat.id
        

        get_data.change_percent(percent,coin,chat_id)
        text = f"✅ Done! You changed the percent for <b>{coin}</b> to <b>{percent}</b>"

        bot.reply_to(message,text=text,parse_mode='HTML')

        logger.info(f"User {chat_id} updated {coin} to {percent}%")
    except Exception as e:
        logger.error(f"change is failed \n {e}")
        bot.reply_to(message,f"{parts[1].lower()} is invalid")
  



@bot.message_handler(commands=['price'])
def cmd_view(message:Message) -> None:
    parts = message.text.split()
    
    if len(parts) < 2:
        bot.reply_to(
            message, 
            "Usage: /price &ltcoin_name&gt;\nExample: <code>/price bitcoin</code>",
            parse_mode='HTML')
        return
    
    coin = parts[1]
    if coin not in SUPPORTED_COINS:
        bot.reply_to(message, f"I don't track {coin}. Try: {', '.join(SUPPORTED_COINS)}")
        return
    
    for c, p in get_data.view(): #[('bitcoin', 81964.0), ('ethereum', 2339.34), ('solana', 97.76)] 
        if c == coin:
            price = p
    bot.reply_to(message, f"price {coin}: {price}" )        




def check_prices_loop() -> None:
    alerts = get_data.get_alerts()

    for change, chat_id, coin, old_price in alerts:
        msg = f"You're coins {get_data.translate_coin(coin)} to exceed the threshold {change}\n"
        try:
            bot.send_message(chat_id=chat_id,text=msg)
        except ApiTelegramException as e:
            logger.error(f"Telegram error: {e}")
        time.sleep(10)




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




if __name__ == '__main__':
    print("starts work")
    #threading.Thread(target=check_prices_loop, daemon=True).start()
    bot.infinity_polling() 
