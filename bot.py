import time
import threading
from sqlite3 import Error

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
        f"Hello, {user_name if not user_name is None else "user"}" 
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
        print(f"beda: {e}")




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
   



@bot.message_handler(commands=['price'])
def cmd_view(message:Message) -> None:
    parts = message.text.split()
    
    if len(parts) < 2:
        bot.reply_to(
            message, 
            "Usage: /price &ltcoin_name&gt;\nExample: <code>/price bitcoin</code>`",
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

    for change, chat_id, coin, old_price, new_price in alerts:
        msg = f"You're coins {get_data.translate_coin(coin)} to exceed the threshold {change}\n"
        try:
            bot.send_message(chat_id=chat_id,text=msg)
        except ApiTelegramException as e:
            print("beda: {e}")
        time.sleep(10)


@bot.message_handler(commands=['button'])
def cmd_button_message(message: Message) -> None:
    # Створюємо клавіатуру
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Створюємо кнопкуVALUES (?, ?)", coins)

    item1 = KeyboardButton("/start")
    item2 = KeyboardButton("/crypto_sub")
    
    
    markup.add(item1)
    markup.add(item2)

    bot.send_message(
        chat_id=message.chat.id, 
        text='Choose what you need', 
        reply_markup=markup
    )


if __name__ == '__main__':
    print("starts work")
    threading.Thread(target=check_prices_loop, daemon=True).start()
    bot.infinity_polling() 
