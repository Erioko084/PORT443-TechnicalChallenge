""""
Author: Erioko084
Python version: 3.9
This is a Python script to create a Telegram chat bot that replies with a dad joke when a user says hello

Source documentation:
python-telegram-bot (Telegram API wrapper for Python):
https://github.com/python-telegram-bot/python-telegram-bot

dadjokes (Dadjokes.io API wrapper for Python):
https://github.com/DadJokes-io/Dad_Jokes_API#getting-started
"""

import os
from dotenv import load_dotenv
from dadjokes import Dadjoke
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

def start(update: Update, context: CallbackContext) -> None:
    # Welcomes user and prompts them to use /help command.

    user = update.effective_user
    new_line = '\n'

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! {new_line}For usage instructions, type /help'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    # Instructs the user on usage

    update.message.reply_text('Usage: Say \"Hello\" for dad joke')

def send_dadjoke(update: Update, context: CallbackContext) -> None:

    # Retrieve a random joke from dadjokes.io
    dad_joke = Dadjoke().joke

    # Sends the dad joke if user says "Hello" (case insensitive), else user is prompted to use /help command.
    if update.message.text.lower() == 'hello':
        update.message.reply_text(dad_joke)
    else:
        update.message.reply_text('For usage instructions, type /help')
def main():

    # Get token for telegram API from environmental variable to prevent leaking it on Git
    load_dotenv()
    API_TOKEN = os.getenv('API_TOKEN')

    # Create updater object and introduce dispatcher
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    # Setup logging module
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Register commands with command handler to listen for /start and /help commands
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))

    # Allow message handler to listen to normal messages and respond accordingly
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_dadjoke))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


