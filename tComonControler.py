#! C:\Users\Алексей\PycharmProjects\YamlContractParser\python-virtual-environments\env python
import logging
import os

import telebot
from telebot.types import Message

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

print(help(os.getenv))
API_TOKEN = '864783318:AAG173kN2JGCSoGVil3Rld2OdV8csamdthI'

bot = telebot.TeleBot(API_TOKEN)
telebot.apihelper.proxy = {'https': 'https://127.0.0.1:9080'}

aboutBotText = "Я - простой бот для парсинга YAML контрактов. \nОснованный на Swagger Open API Specification. \nДля " \
               "начала - просто брось мне YAML-файл. "


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: Message):
    user = message.from_user.username
    bot.reply_to(message, f'Привет, {user}! \n {aboutBotText}')


@bot.message_handler(content_types=['text'])
def send_welcome(message: Message):
    user = message.from_user.username
    bot.reply_to(message, f'Hellow, {user}')


if __name__ == '__main__':
    bot.polling(none_stop=True)
