#! C:\Users\Алексей\PycharmProjects\YamlContractParser\python-virtual-environments\env python
import logging
import pickle

import requests
import telebot
import yaml
from telebot import types
from telebot.types import Message

import dataControler
from config import load_config

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
proxies = load_config()[1]
API_TOKEN = load_config()[0]
bot = telebot.TeleBot(API_TOKEN)
telebot.apihelper.proxy = proxies

# TODO: перенести текстовки сообщений в конфиг
aboutBotText = 'Я - простой бот для парсинга YAML контрактов. \nОснованный на Swagger Open API Specification. ' \
               '\nДля начала работы введи команду /start или просто брось мне YAML-файл.' \
               '\nДля информации о возможностях и ограничениях бота введи команду /help.'

startBotText = 'Для начала работы отправь мне YAML-файл контракта. \n Получаемые данные нигде не сохраняются.'

helpBotText = 'не поддерживается следующие keywords: allOf, anyOf, Links'

msgTypes = {
    'Входящие параметры': 'Request',
    'Исходящие параметры': 'Response',
    'Все параметры': 'All'
}

pathTypes = {
    'paths': 'paths',
    'operationId': 'operationId'
}


class ContextForParse:
    def __init__(self, msgType: str = list(msgTypes.values())[0], pathType: str = list(pathTypes.values())[0]):
        self.msgType = msgType
        self.pathType = pathType


context = ContextForParse()


@bot.message_handler(content_types=['document'])
def common_doc_handler(message: Message):
    if message.content_type == 'document' and message.document.mime_type == 'application/x-yaml':
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        file = requests.get(f'https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}',
                            proxies=proxies, stream=True, timeout=60)
        data = yaml.safe_load(file.text)
        with open(f'temp_contracts\contract_{message.chat.id}.yaml', 'wb') as f:
            pickle.dump(data, f)
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton(list(msgTypes.keys())[0])
        itembtn2 = types.KeyboardButton(list(msgTypes.keys())[1])
        itembtn3 = types.KeyboardButton(list(msgTypes.keys())[2])
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, "Выбирете тип параметров:", reply_markup=markup)


@bot.message_handler(commands=['start', 'help', 'about'])
def common_comand_handler(message: Message):
    user = message.from_user.username
    if message.text == '/start':
        bot.reply_to(message, f'Привет, {user}! \n {startBotText}')
    elif message.text == '/help':
        bot.reply_to(message, f'{user}, вот что ты должен знать о моих возможностях: \n {helpBotText}')
    elif message.text == '/about':
        bot.reply_to(message, f'{user}, вот что ты должен знать обо мне: \n {aboutBotText}')


@bot.message_handler(func=lambda message: message.text in msgTypes.keys(), content_types=['text'])
def common_result_handler_1(message):
    context.msgType = msgTypes[message.text]
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton(list(pathTypes.keys())[0])
    itembtn2 = types.KeyboardButton(list(pathTypes.keys())[1])
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Выбирете тип paths\operationId:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in pathTypes.keys(), content_types=['text'])
def common_result_handler_2(message):
    with open(f'temp_contracts\contract_{message.chat.id}.yaml', 'rb') as f:
        data = pickle.load(f)
    context.pathType = pathTypes[message.text]
    parsedData = dataControler.getDataContract(data, contextParams=context.msgType, contextPath=context.pathType)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton(list(msgTypes.keys())[0])
    itembtn2 = types.KeyboardButton(list(msgTypes.keys())[1])
    itembtn3 = types.KeyboardButton(list(msgTypes.keys())[2])
    markup.add(itembtn1, itembtn2, itembtn3)
    i = 0
    fullMsg = ''
    while i < len(parsedData):
        if parsedData[i][1] is not None:
            msg = '*' + parsedData[i][0] + '*' + '    ' + '_' + parsedData[i][1] + '_'
        else:
            msg = '*' + parsedData[i][0] + '*'
        i += 1
        fullMsg = fullMsg + msg + '\n'
    if fullMsg != '':
        bot.reply_to(message, text=fullMsg, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.reply_to(message, f'{message.text} отсутствуют', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
