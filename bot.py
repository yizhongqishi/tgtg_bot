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
send = False


def start(update: Update, context: CallbackContext):
    global state
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! My current state is {}".format(state))
    logging.info("this user {}".format(update.effective_chat.id))


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def add_notion(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="OKOK")
    logging.info("New ID:"+str(update.effective_chat.id))


def send_notion():
    with open("id.list", "r") as f:
        ids = f.readlines()
        for id in ids:
            bot.send_message(chat_id=int(id), text="New Items!")


def send_alert(mes="Something Wrong!"):
    with open("admin.id", "r") as f:
        admin_id = f.readline()
        bot.send_message(chat_id=int(admin_id), text=mes)


def check_again(update: Update, context: CallbackContext):
    global send
    send = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="OK, will watch that for you")


def daytime():
    now = datetime.datetime.now()
    result = (now.hour * 100) + now.minute
    return result


def tg_client():
    sleep_from = 1915
    sleep_to = 1200
    global send
    global state
    with open("tg.token", "r") as f:
        data = json.load(f)
    client = TgtgClient(access_token=data["access_token"], refresh_token=data["refresh_token"], user_id=data["user_id"])
    logging.info("I'm going to work")
    while True:
        now = daytime()
        if now >= sleep_from or now <= sleep_to or send:
            if now >= sleep_from or now <= sleep_to:
                send = False
            logging.info("Sleeping Time")
            send_alert("I'm Sleeping")
            state = "Sleeping"
            while now >= sleep_from or now <= sleep_to or send:
                logging.info("Current time is {}, still sleeping".format(now))
                time.sleep(60)
                now = daytime()
            logging.info("Current time is {}, time to wake up".format(now))
            send_alert("Wake up now")
            state = "Watching"
        try:
            item = client.get_item(600644)
            if item['items_available'] > 0:
                logging.info("New things, hurry up!")
                send_notion()
                send = True
            else:
                time.sleep(random.randrange(50, 60))
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

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    tg_client()
    updater.stop()
