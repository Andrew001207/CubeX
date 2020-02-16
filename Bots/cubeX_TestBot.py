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
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Read configfile
config = configparser.ConfigParser()

config_filename = ".bot.conf"
config.read(config_filename)

username = input('please insert your username: ')
try:
    bot_token = config[username]['token']
    token_tuple = config[username]['token_tuple']
except KeyError:
    bot_token = input('''please insert you token from Botfather or create a ~/CubeX/Bots/.bot.conf file like this
[<username>]
token=<token>
''')

logger.info('Read config')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def create_task(update, context):
    """Create a new task for the Cube"""
    task = ""
    group = ""
    #def i_start(update, context):
    def i_start(bot, update):
        update.message.reply_text("Enter name")
        return SET_NAME

    def i_name(update, context):
        task = update.message.text
        update.message.reply_text("Enter group")
        return SET_GROUP

    def i_group(update, context):
        group = update.message.text
        update.message.reply_text("Done")
        return ConversationHandler.END
    #task = ask_user(update, context, "Please enter task name")
    #group = ask_user(update, context, "Got it! Now enter the group of the task")
    #update.message.reply_text(f'Created task {task} of group {group}.')
    START, SET_NAME, SET_GROUP = range(3)
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^[a-zA-Z]$'), i_start)],

        states={
            SET_NAME: [MessageHandler(Filters.text, i_name)],

            SET_GROUP: [MessageHandler(Filters.text, i_group)]
        },

        fallbacks=[CommandHandler("error", error)]
    )
    context.dispatcher.add_handler(conv_handler)

    conv_handler.handle_update(update, context.dispatcher, (conv_handler._get_key(update), MessageHandler(Filters.regex('^$'), i_start),re.match('^$','')))
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)

def ask_user(update, context, question):
    update.message.reply_text(question)
    msg_id = update.message.message_id
    print("Before: ", update.message.message_id, context.bot.getUpdates[-1].update_id)
    while(msg_id == update.message.message_id):
        pass
    print("After: ", update.message.message_id)
    return update.message.text


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    #import pdb; pdb.set_trace()
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(CommandHandler("ct", create_task))

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
