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


TASK_NAME, TASK_TEXT, TASK_GROUP, TASK_FINISH = range(4)
task_list = [] 

class Task():
    def __init__(self):
        self.name = ''
        self.text = ''
        self.group = ''


cur_task = Task()


def create_task_name(update, context):
    update.message.reply_text('Please insert the name of the new Task')
    return TASK_TEXT


def create_task_text(update, context):
    update.message.reply_text('Please insert a description  of the new Task')
    cur_task.name = update.message.text
    return TASK_GROUP


#NOTE: show we use a compositum pattern for task. So we don't have to treat groups differently
def create_task_group(update, context):
    #TODO: Make it possible to add the Task to more groups
    update.message.reply_text('Please insert a groupe in with the the new Task should be a part of.')
    cur_task.text = update.message.text
    return TASK_FINISH


def finish_task_creation(update, context):
    cur_task.group = update.message.text
    task_list.append(cur_task)
    #cur_task = Task() TODO: replace this, so more task can be created
    update.message.reply_text('The task "%s" has been succesfully created.' % cur_task.name)
    print(cur_task.name)
    print(cur_task.text)
    print(cur_task.group)


def start(update, context):
    update.message.reply_text('Welcome to the cube bot')
    return TASK_NAME


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


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
            TASK_NAME: [MessageHandler(Filters.text, create_task_name)],
            TASK_TEXT: [MessageHandler(Filters.text, create_task_text)],
            TASK_GROUP: [MessageHandler(Filters.text, create_task_group)],
            TASK_FINISH: [MessageHandler(Filters.text, finish_task_creation)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

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
