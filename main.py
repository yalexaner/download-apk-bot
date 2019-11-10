# coding=utf-8

import telebot
from telebot import types
import os
from flask import Flask, request

from apk import Apk
import messages

bot = telebot.TeleBot(os.environ['telegram_token'])

server = Flask(__name__)

apk = Apk()

@bot.message_handler(commands=['start'])
def start(message):
    # bot.send_message(message.chat.id, messages.hello, reply_markup=types.ReplyKeyboardHide())
    bot.send_message(message.chat.id, messages.hello)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, messages.help)
    # bot.send_message(message.chat.id, messages.help, reply_markup=types.ReplyKeyboardHide())

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, messages.about)

@bot.message_handler(content_types=['text'])
def get_url(message):
    url = apk.find(message.text)
    # bot.send_message(message.chat.id, url, reply_markup=types.ReplyKeyboardHide())

    if url:
        bot.send_message(message.chat.id, url)
    else:
        bot.send_message(message.chat.id, 'Sorry. There\'s no such file in there')

@server.route("/bot", methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="{}/bot".format(os.environ['app_url']))
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
