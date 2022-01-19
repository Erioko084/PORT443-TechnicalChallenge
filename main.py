# Author:
# This is a Python script to create a Telegram chat bot that replies with a dad joke when a user says hello

# source documentation
# https://github.com/python-telegram-bot/python-telegram-bot
# https://github.com/DadJokes-io/Dad_Jokes_API#getting-started

import os
from dotenv import load_dotenv
from dadjokes import Dadjoke
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Get API key for telegram API from environmental variable to prevent leaking it on Git
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    # Welcomes user and prompts them to use /help command.
    user = update.effective_user
    new_line = '\n'
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! {new_line}For usage instructions, type /help'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Usage: Say \"Hello\" for dad joke')

def send_dadjoke(update: Update, context: CallbackContext) -> None:
    # Sends dad joke if user says "Hello" (case insensitive), else user is prompted to use /help command.

    dadjoke = Dadjoke().joke

    if update.message.text.lower() == 'hello':
        update.message.reply_text(dadjoke)
    else:
        update.message.reply_text('For usage instructions, type /help')
def main():

    updater = Updater(API_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_dadjoke))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()


