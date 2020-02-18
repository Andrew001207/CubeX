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
import re, automat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler


#NOTE: is there a nicer way than global?
curr_cube_id = None

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
except KeyError:
    bot_token = input('''please insert you token from Botfather or create a ~/CubeX/Bots/.bot.conf file like this
[<username>]
token=<token>
and insert your username and token ther
''')

logger.info('Read config')

class Conv_automat():
    '''example: 
    state_name = ('question', {'maping of answers':'to new state'}'''
    stats = {'start':('do you have a cube', {'ja':self.select_cube, 'nein':self.create_cube,'else':}),
            'select_cube':(lamda : self.get_cube_list())
            }
    state_texts = {self.start:'give the task a name: ',
            self.group:'give the task a group: '}
    def __init__(self):
        self.last_state = None
        self.curr_state = self.start
        self.next_state = self.group
    def interpret_text(self, update, context):
        answer = update.message.text
        self.curr_state(answer) # her the function has to set the next_state

        if isinstanc(state_texts[self.next_state], str):
            update.message.reply_text = state_texts[self.next_state]
        else:
            update.message.reply_text = state_texts[self.next_state]()

        self.curr_state = self.next_state
        self.next_state = None # the function will have to set this, based of the users answer or her desision


    def start(self, answer):

        return ('do you have a cube', {'ja':self.select_cube, 'nein':self.create_cube})
    def select_cube(self):
        return (None, {'default': self.end_conv})

    def end_conv(self)
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # create a instanc of the conversation automat:
    ca = Conv_automat()
    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(Filters.regex('^[a-zA-Z0-9]'), ca.interpret_text)
    dp.add_handler(CommandHandler(Filters.regex('^[a-zA-Z0-9]'), ca.interpret_command)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # command to create new task
    dp.add_handler(CommandHandler("ct", create_task))

    # command to select current cube
    dp.add_handler(CommandHandler("sc", select_cube))

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
