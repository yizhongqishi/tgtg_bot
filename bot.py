from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
from pprint import pprint
import json
from tgtg import TgtgClient
import time
import random
import datetime


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome!")
    pprint(update.effective_chat.id)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def add_notition(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OKOK")
    logging.info("New ID:"+str(update.effective_chat.id))


def send_notition():
    with open("id.list", "r") as f:
        ids = f.readlines()
        for id in ids:
            bot.send_message(chat_id=int(id), text="New Items!")


def send_alert():
    with open("admin.id", "r") as f:
        admin_id = f.readline()
        bot.send_message(chat_id=int(admin_id), text="Something Wrong!")


def daytime():
    now = datetime.datetime.now()
    nowint = (now.hour * 100) + now.minute
    return nowint


def tg_clinet():
    with open("tg.token", "r") as f:
        data = json.load(f)
    client = TgtgClient(access_token=data["access_token"], refresh_token=data["refresh_token"], user_id=data["user_id"])
    send = False
    while True:
        now = daytime()
        if now >= 1915 or now <= 1200:
            logging.info("Sleeping Time")
            while now >= 1915 or now <= 1200:
                now = daytime()
                time.sleep(600)
            logging.info("Time to Wake Up")
            send = False
        if send:
            now = daytime()
            while now < 1915:
                time = time.sleep(36000)
        try:
            item = client.get_item(600644)
            if item['items_available'] > 0:
                logging.info("New things, hurry up!")
                send_notition()
                send = True
            else:
                time.sleep(random.randrange(50, 60))
        except Exception as e:
            logging.error(e)
            send_alert()
            break



if __name__ == "__main__":
    with open("bot.token", "r") as f:
        token = f.readline().replace("\n", "")
    updater = Updater(token=token, use_context=True)
    bot = updater.bot
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater.start_polling()

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    add_handler = CommandHandler("addme", add_notition)
    dispatcher.add_handler(add_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    tg_clinet()
    updater.stop()






