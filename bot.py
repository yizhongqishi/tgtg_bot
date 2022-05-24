from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
import os
import json
from tgtg import TgtgClient
import time
import random
import datetime


send = False
sleep_from = 1917
sleep_to = 900
item_id = 600644
ss = False


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! My current state is {}".format(state))
    logging.info("this user is {}".format(update.effective_chat.id))


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def add_notion(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OKOK")
    logging.info("Please Add New ID:"+str(update.effective_chat.id))


def stop(update: Update, context: CallbackContext):
    global ss
    context.bot.send_message(chat_id=update.effective_chat.id, text="See You Soon!".format(state))
    ss = True
    os._exit(0)


def send_notion(mes="New Items!", user="common"):
    with open(user+'.list', "r") as f:
        ids = f.readlines()
        for id in ids:
            bot.send_message(chat_id=int(id), text=mes)


def send_alert(mes="Something Wrong!"):
    send_notion(mes, "admin")


def check_again(update: Update, context: CallbackContext):
    global send
    send = False
    now = daytime()
    if now >= sleep_from or now <= sleep_to:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Out of business hours!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="OK, will watch that for you")


def daytime():
    now = datetime.datetime.now()
    result = (now.hour * 100) + now.minute
    return result


def send_station(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="the send station is {}".format(send))


def tg_client():
    global send
    global state
    with open("tg.token", "r") as f:
        data = json.load(f)
    client = TgtgClient(access_token=data["access_token"], refresh_token=data["refresh_token"], user_id=data["user_id"])
    logging.info("I'm going to work")
    while True:
        if ss:
            break
        now = daytime()
        if now >= sleep_from or now < sleep_to or send:
            state = "Sleeping"
            while now >= sleep_from or now <= sleep_to or send:
                send = (sleep_to < now < sleep_from)
                t = 60
                if not send:
                    if now >= sleep_from:
                        t = (23 - (now // 100)) * 100 + 60 - (now % 100) + sleep_to
                    else:
                        t = sleep_to - now
                    t = t // 100 * 3600 + (t % 100) * 60
                logging.info("Current time is {}, will sleep {} hrs ({} mins)".format(now, t / 3600, t // 60))
                time.sleep(t)
                now = daytime()
            send_notion("Wake up now")
            state = "Watching"
        try:
            item = client.get_item(item_id)
            if item['items_available'] > 0:
                logging.info("New things, hurry up!")
                send_notion()
                state = "Sleeping"
                send_notion("I'm Sleeping")
                send = True
            else:
                time.sleep(random.randrange(20, 30))
        except Exception as e:
            logging.error(e)
            send_alert()
            break


if __name__ == "__main__":
    send = False
    state = "Watching"
    with open("bot.token", "r") as f:
        token = f.readline().replace("\n", "")
    updater = Updater(token=token, use_context=True)
    bot = updater.bot
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater.start_polling()

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    add_handler = CommandHandler("addme", add_notion)
    dispatcher.add_handler(add_handler)

    check_handler = CommandHandler("still", check_again)
    dispatcher.add_handler(check_handler)

    stop_handler = CommandHandler("stop", stop)
    dispatcher.add_handler(stop_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    tg_client()
    updater.stop()
