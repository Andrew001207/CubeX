#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, configparser

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# Read configfile
config = configparser.ConfigParser()

config_filename = ".bot.conf"
config.read(config_filename)

username = input('please insert you username')
bot_token = config[username]['token']

logger.info('Read config')
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def create_cube(update, context):
    update.message.replay_text('Please select the number of sides the cube should have')
    update.massage.from_user()
#def select_cube()

#def create_task() done
##NOTE: show we use a compositum pattern for task. So we don't have to treat groups differently

## different mapping from tasks to sides according to context:
#def create_context()
#class cube()
#    def get_task()
#    def map_task()
#    def get_current_side()
#    def _change_side()


def cool(update, context):
    print('cool')

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    context


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cool", cool))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()