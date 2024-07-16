import os;
from dotenv import dotenv_values;
import telebot;

config = dotenv_values(".env");

BOT_TOKEN = config['BOT_TOKEN'];

bot = telebot.TeleBot(BOT_TOKEN);

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?");

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text);

bot.infinity_polling();
