import telebot
from telebot import apihelper
import requests

import urllib

api_id = ####
api_hash = ####

token = ####
chat_id = ####
pr = {'https': 'https://200.73.128.5:3128'}
apihelper.proxy = pr

s = requests.Session()
res = s.get('https://api.telegram.org/bot{0}/deletemessage?message_id={1}&chat_id={2}'.format(token, 3, chat_id), proxies=pr)
print(res)
#def delete_message(id):
#bot = telebot.TeleBot(token)
#lol = bot
#print(lol)
#bot.get_updates()
#bot.delete_message(chat_id, '2')
#bot.polling()