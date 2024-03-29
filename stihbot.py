from os import environ
config = environ.get('CONFIG', 'poetry.json')

from tendo import singleton
me = singleton.SingleInstance(flavor_id=config)

import logging

logging.basicConfig(filename=f"{config}.log", level=logging.INFO)
logger = logging.getLogger(__name__)

import json
data = json.load(open(config))

import requests
url = data['url']
length = data['length']
model = data['model'] 

def get_sample(text):
    response = requests.post(url, json={"prompt": text, "model": model, "length": length, "num_samples": 1, "allow_linebreak": True})

    logger.info(response)
    return json.loads(response.text)["replies"][0]

import telebot

bot = telebot.TeleBot(data['bot_key'], num_threads=20)

from telebot import apihelper

#apihelper.proxy = {'https':data['proxy_str']}

def message_handler(message):
    logger.info(message.from_user)
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = get_sample(message.text)
        if 'poetry' not in url:
            response = f'_{message.text}_{response}'
        bot.reply_to(message, response, parse_mode="Markdown")
    except telebot.apihelper.ApiException as e:
        print(e)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Присылай начало, а я продолжу")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    message_handler(message)
    
@bot.channel_post_handler(func=lambda m: True)
def echo_all(message):
    message_handler(message)

bot.polling()


