# kittybot/kittybot.py
import logging
import os
import requests

from telebot import TeleBot, types
from dotenv import load_dotenv


load_dotenv()

secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'
COMPLIMENT_URL = 'https://tools-api.robolatoriya.com/compliment'


# Код запроса к thecatapi.com и обработку ответа обернём в функцию:
def get_new_cat():
    try:
        response = requests.get(CAT_URL)
        response.raise_for_status()
        response = response.json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = DOG_URL
        response = requests.get(new_url)
        response = response.json()

    random_cat = response[0].get('url')
    return random_cat


def get_new_dog():
    try:
        response = requests.get(DOG_URL)
        response.raise_for_status()
        response = response.json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = CAT_URL
        response = requests.get(new_url)
        response = response.json()

    random_dog = response[0].get('url')
    return random_dog


def get_compliment():
    response = requests.get(COMPLIMENT_URL)
    response = response.json()
    return response


# Добавляем хендлер для команды /newcat:
@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_cat())


# Добавляем хендлер для команды /newdog:
@bot.message_handler(commands=['newdog'])
def new_dog(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_dog())


# Добавляем хендлер для команды /compliment:
@bot.message_handler(commands=['compliment'])
def new_compliment(message):
    chat = message.chat
    bot.send_message(chat.id, get_compliment())


@bot.message_handler(commands=['start'])
def wake_up(message):
    # В ответ на команду /start
    # должно быть отправлено сообщение "Спасибо, что включили меня".
    chat = message.chat
    name = chat.first_name
    chat_id = chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('/newcat'),
                 types.KeyboardButton('/newdog'))
    keyboard.row(types.KeyboardButton('/compliment'))
    bot.send_message(
        chat_id=chat_id,
        text=f'Спасибо, что включили меня, {name}!',
        reply_markup=keyboard
        )
    bot.send_message(chat_id=chat_id,
                     text=f'Смотри, какой котик {name}!',
                     reply_markup=keyboard)
    bot.send_photo(chat.id, get_new_cat())
    bot.send_message(chat_id=chat_id,
                     text=f'Смотри, какой пёсик {name}!',
                     reply_markup=keyboard)
    bot.send_photo(chat.id, get_new_dog())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    # Из объекта message получаем данные о чате, из которого пришло сообщение,
    # и сохраняем эти данные в переменную chat.
    chat = message.chat
    # Получаем id чата:
    chat_id = chat.id
    # В ответ на любое текстовое сообщение в тот же чат
    # будет отправлено сообщение 'Привет, я KittyBot!'
    bot.send_message(chat_id=chat_id, text='Привет, я DimonoBot!')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
