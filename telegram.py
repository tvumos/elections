import telebot
from telebot import apihelper
import time
import csv

TKN = 'key'


bot = telebot.TeleBot(TKN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    bot.process_new_channel_posts("Привет")



# ' api.telegram.org'

# def create_connect():
#     with open('proxy_export.csv', newline='') as File:
#         reader = csv.reader(File)
#         for row in reader:
#             row_arr = row[0].split(';')
#             print(row[0], " | ", row_arr[2])

proxies = {
    'http': 'http://185.186.81.250:4145',
    'https': 'http://185.186.81.250:4145',
}

apihelper.proxy = proxies

# apihelper.

bot.polling()
