#! C:\Users\Алексей\PycharmProjects\YamlContractParser\python-virtual-environments\env python
import logging

import requests
import telebot
import yaml
from telebot.types import Message

import main
from settings import API_TOKEN, proxies

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)
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
        file = requests.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}',
                            proxies=proxies, stream=True)
        data = yaml.safe_load(file.text)
        parsedData = main.getDataContract(data)
        i = 0
        while i < len(parsedData):
            if parsedData[i][1] is not None:
                msg = parsedData[i][0] + ' <b>' + parsedData[i][1] + '</b>'
            else:
                msg = parsedData[i][0] + ' '
            bot.send_message(message.chat.id, text=msg, parse_mode='HTML')
            i += 1
    elif message.text == '/start':
        bot.reply_to(message, f'Привет, {user}! \n {startBotText}')
    elif message.text == '/help':
        bot.reply_to(message, f'{user}, вот что ты должен знать о моих возможностях: \n {helpBotText}')
    elif message.text == '/about':
        bot.reply_to(message, f'{user}, вот что ты должен знать обо мне: \n {aboutBotText}')


if __name__ == '__main__':
    bot.polling(none_stop=True)
