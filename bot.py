from sqlite3 import Error
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

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
        "\n/price" \
            )
    

    bot.reply_to(message=message, text=text)
    try:
        get_data.add_user_info(chat_id, user_name if user_name else "user")

    except Error as e:
        print(f"beda: {e}")



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
    bot.infinity_polling() 
