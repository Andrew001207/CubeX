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

username = 'kilian'
bot_token = config[username]['token']

logger.info('Read config')
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

class Task():
    pass
#def create_task()
##NOTE: show we use a compositum pattern for task. So we don't have to treat groups differently
#def create_task_group
## different mapping from tasks to sides according to context:
#def create_context()

CUBES, TASKS = range(2)

class Cube():
    def __init__(self, side_amount):
        self.current_side = self.get_current_side()
        #QUESTION: is there a elegant way to do this:
        self.sides = {}
        for el in range(side_amount):
            self.sides[el] = []

#    def get_task()
    def map_task(self, side, task):
        self.sides[side].append(task)
    def get_current_side(self):
        #TODO:
        return 0
#    def _change_side()

def create_cube(update, context):
    update.message.replay_text('Please select the number of sides the cube should have')
    update.massage.from_user()

def select_cube(update, context):
    reply_keyboard = [['6', '8', '20']]

    update.message.reply_text('start replay',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    sides = update.message.from_user()
    #TODO: make cube not global.?
    cube = Cube(sides)
    return TASKS



# create dummy:
cube = Cube(0)

def cool(update, context):
    print('cool')

def start(update, context):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text('start replay',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CUBES

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


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

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CUBES: [MessageHandler(Filters.regex('^(6|12|20)$'), select_cube)],

            TASKS: [MessageHandler(Filters.text, cube.map_task)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # on different commands - answer in Telegram
#    dp.add_handler(CommandHandler("start", start))
#    dp.add_handler(CommandHandler("help", help))
#    dp.add_handler(CommandHandler("cool", cool))

    # on noncommand i.e message - echo the message on Telegram
#    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_handler(conv_handler)

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
