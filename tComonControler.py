#! C:\Users\Алексей\PycharmProjects\YamlContractParser\python-virtual-environments\env python
import logging
import urllib
from urllib import request

import requests
import telebot
import yaml
from telebot.types import Message

import main

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN = '864783318:AAG173kN2JGCSoGVil3Rld2OdV8csamdthI'
# TODO: перенести в переменные окружения

bot = telebot.TeleBot(API_TOKEN)
proxies = {
    'https': 'https://127.0.0.1:9080'
}
telebot.apihelper.proxy = proxies

aboutBotText = 'Я - простой бот для парсинга YAML контрактов. \nОснованный на Swagger Open API Specification. ' \
               '\nДля начала работы введи команду /start или просто брось мне YAML-файл.' \
               '\nДля информации о возможностях и ограничениях бота введи команду /help.'

startBotText = 'Для начала работы отправь мне YAML-файл контракта. \n Получаемые данные нигде не сохраняются.'

helpBotText = 'не поддерживается следующие keywords: allOf, anyOf, Links'


@bot.message_handler(commands=['start', 'help', 'about'])
@bot.message_handler(content_types=['document'])
def handle_start_help(message: Message):
    user = message.from_user.username
    if message.content_type == 'document' and message.document.mime_type == 'application/x-yaml':
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        proxy = urllib.request.ProxyHandler({'http': 'https://127.0.0.1:9080'})
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path),
                            proxies=proxies, stream=True)
        data = yaml.safe_load(file.text)
        parsedData = main.getDataContract(data)
        bot.reply_to(message, parsedData)
        # TODO Исправить: в сообщении возвращается только первый элемент первого кортежжа из списка
    elif message.text == '/start':
        bot.reply_to(message, f'Привет, {user}! \n {startBotText}')
    elif message.text == '/help':
        bot.reply_to(message, f'{user}, вот что ты должен знать о моих возможностях: \n {helpBotText}')
    elif message.text == '/about':
        bot.reply_to(message, f'{user}, вот что должен знать обо мне: \n {aboutBotText}')


if __name__ == '__main__':
    bot.polling(none_stop=True)
