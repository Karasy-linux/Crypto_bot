from sqlite3 import Error
import time
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
        "\n/subcribes"
        "\n/prices" \
            )
    

    bot.reply_to(message=message, text=text)
    try:
        get_data.add_user_info(chat_id, user_name if user_name else "user")

    except Error as e:
        print(f"beda: {e}")




@bot.message_handler(commands=['subcribes'])
def cmd_crypto_sub(message: Message) -> None:
    text = (
        "subscribe to coins:"
        "\n /bitcoin"
        "\n /ethereum"
        "\n /solana"
        )
    
    bot.reply_to(message=message,text=text)




@bot.message_handler(commands=['bitcoin'])
def cmd_bitcoin(message: Message) -> None:
    get_data.subscribe(message.chat.id,'bitcoin')
    text = f"You're monitoring bitcoin"

    bot.reply_to(message=message,text=text)





@bot.message_handler(commands=['ethereum'])
def cmd_ethereum(message: Message) -> None:
    get_data.subscribe(message.chat.id,'ethereum')
    text = f"You're monitoring bitcoin"

    bot.reply_to(message=message,text=text)




@bot.message_handler(commands=['solana'])
def cmd_solana(message: Message) -> None:
    get_data.subscribe(message.chat.id,'solana')
    text = f"You're monitoring bitcoin"

    bot.reply_to(message=message,text=text)
    
@bot.message_handler(commands=['prices'])
def cmd_view(message:Message) -> None:
    viewers = get_data.viewing()
    text = f"{viewers}"

    bot.reply_to(message=message,text=text)

@bot.message_handler(commands=['button'])
def cmd_button_message(message: Message) -> None:
    # Створюємо клавіатуру
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Створюємо кнопкуVALUES (?, ?)", coins)

    item1 = KeyboardButton("/start")
    item2 = KeyboardButton("/crypto_sub")
    
    
    # Додаємо кнопку в розмітку
    markup.add(item1)
    markup.add(item2)
    # Відправляємо повідомлення (ПЕРЕВІР ДУЖКИ!)
    bot.send_message(
        chat_id=message.chat.id, 
        text='Choose what you need', 
        reply_markup=markup
    )




if __name__ == '__main__':
    print("starts work")
    bot.infinity_polling() 
