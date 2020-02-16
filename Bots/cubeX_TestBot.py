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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()

config_filename = ".bot.conf"

config.read(config_filename)

username = 'maxdi'
bot_token = config[username]['token']

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
    task = None
    group = None
    SET_NAME, SET_GROUP = range(2) #Constants for ConversationHandler
    
    def i_start(update, context):
        """
        Start creating new task
        
        Returns:
        int: next state for ConversationHandler
        """
        update.message.reply_text("Enter name")
        return SET_NAME

    def i_name(update, context):
        """
        Read the entered name of the new task
        
        Returns:
        int: next state for ConversationHandler
        """
        nonlocal task
        task = update.message.text
        update.message.reply_text("Enter group")
        return SET_GROUP

    def i_group(update, context):
        """
        Read the entered group of the new task and finish creation of the new task
        
        Returns:
        int: next stop-state for ConversationHandler
        """
        nonlocal task
        nonlocal group
        group = update.message.text
        #Insert actual code to create task
        update.message.reply_text(f'Created task {task} in group {group}.')
        #Reset handlers
        context.dispatcher.remove_handler(conv_handler)
        return ConversationHandler.END
    
    conv_handler = ConversationHandler(
        #Workaround to automatically start ConversationHandler
        entry_points=[MessageHandler(Filters.text, i_start)],

        states={
            SET_NAME: [MessageHandler(Filters.text, i_name)],

            SET_GROUP: [MessageHandler(Filters.text, i_group)]
        },

        fallbacks=[CommandHandler("error", error)]
    )
    context.dispatcher.add_handler(conv_handler)
    #Autostart ConversationHandler
    update_tmp = update
    update_tmp.message.text = "text"
    context.dispatcher.process_update(update_tmp)

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