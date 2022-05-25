#!/usr/bin/env python3
from telegram.ext import *
import responses as R
from random import randrange

import sys

sys.path.append(r'D:\\condatr\\envs\\telegram_bot\\python39.zip')

API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

print("Bot started..")

def start_command(update,context):
    update.message.reply_text("type something to start")
    
def help_command(update,context):
    update.message.reply_text("Temel iletisim, kripto fiyat sorgulama, hava durumu, film öneri, rastgele resim")

    
def print_hi(update,context):
    update.message.reply_text("hello {}".format(randrange(999)))
    
def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)
    
    update.message.reply_text(response)
    
def error(update, context):
    print("Update {} caused error {}").format(update, context.error)
    
def main():
    updater = Updater(API_KEY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("teragron", print_hi))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

    
main()