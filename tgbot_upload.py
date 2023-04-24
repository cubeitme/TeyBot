from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from datetime import datetime
import os
import time
import psutil
import subprocess
from tkinter import filedialog as fd
from tkinter import END
import threading
import selenium
from selenium.webdriver.chrome.options import Options
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from bs4 import BeautifulSoup
import requests

Wheaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
TOKEN = 'TELEGRAM_TOKEN'
YTOKEN = 'YANDEX_DISK_TOKEN'
AdminDataBase = ['ADMIN_TELEGRAM_ID']
DateTime = datetime.now()
timeNow = DateTime.strftime('%H:%M')
dateNow = DateTime.strftime('%m.%d.%Y')
bot = telebot.TeleBot(TOKEN)

def save():
    file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt")), defaultextension='')
    f = open(file_name, 'w')
    s = f.get(1.0, END)
    f.write(s)
    f.close()

@bot.message_handler(commands=['start'])
def start(message):
    try:
        telegram_user = message.from_user
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

        '''keyboard = [
            [
                telebot.types.InlineKeyboardButton("Capture", callback_data='DOsendCapture'),
                telebot.types.InlineKeyboardButton("Video (15)", callback_data='sendVideo15'),
                telebot.types.InlineKeyboardButton("Video (30)", callback_data='sendVideo30'),
                telebot.types.InlineKeyboardButton("Video (60)", callback_data='sendVideo60')
            ],
        ]'''

        bot.send_message(chat_id=message.chat.id,
                         text='Hosted by Tey\n/w [ГОРОД] - Погода\n/s [ЗАПРОС] - Поиск в Google (Времмено не работает)')
    except:
        return
def get_the_weather(city):
    try:
        global weather
        city = city.replace(' ', '+')
        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=Wheaders)
        #print('Searching for weather...\n')                        #Add this command for debug
        soup = BeautifulSoup(res.text, 'html.parser')
        weather = soup.select('#wob_tm')[0].get_text().strip()
        #print(weather + 'C')                                       #Add this command for debug
    except:
        return

@bot.message_handler(commands=['/w'])
def checkplace(message):
    try:
        msg = bot.str(message.text.lower())
        text = msg.replace('/w ', '')
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        get_the_weather(text)
    except:
        return

# Get
@bot.message_handler(commands=['get'])
def get(message):
    try:
        Btext = str(message.text.lower())
        text = Btext.replace('/get ', '')
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if text == '' or text == ' ':
            bot.send_message(chat_id=message.chat.id, text='Tey Bot Documentation')
            bot.send_document(chat_id=message.chat.id, document=open('TeyBotTGConsole.txt', 'r'))
        if text == 'chat info':
            bot.send_message(chat_id=message.chat.id, text='Chat info:\nid: ' + str(message.chat.id))
        if text == 'chat id':
            bot.send_message(chat_id=message.chat.id, text='Chat id:\nid:'+ str(message.chat.id))
    except:
        return

# END
@bot.callback_query_handler(func=lambda call: True)
def button(call):
    globals()[call.data](call.message.chat.id)

def main():
    bot.polling(none_stop=False, interval=5, timeout=20)

if __name__ == '__main__':
    main()