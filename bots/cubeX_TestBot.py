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


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

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
    def __init__(self):
        #self.last_state = None
        self.curr_state = self.start
        self.next_state = None # will be set by the current methode


        self.state_texts = {
                self.side:'please choose a side of the cube',
                self.name:'give the task a name: ',
                self.group:'give the task a group: ',
                self.end : 'task creation finished!',
                'error':self.error
                }

    def handle_answer(self, update, context):

        answer = update.message.text
        
        self.curr_state(answer) # here the function has to set the next_state

        try:
            befor = self.state_texts[self.next_state]
        except KeyError as e:
            # befor = self.state_texts['error']
            # TODO: handel errors better
            self.next_state = end
            befor = 'an error okkured: keyerror'

        if isinstance(befor, str):
            reply = befor
        #TODO: elif callable(befor):
        else:
            reply = befor()

        update.message.reply_text(reply)
        
        logger.debug(f'reply massage for user: {reply}')

        self.curr_state = self.next_state
        self.next_state = None # the function will have to set this, based of the users answer or her desision

        logger.debug(f'changed state to {self.curr_state}')
        return 

    def start(self, answer):
        
        self.next_state = self.name

    def name(self, answer):
        print(f'this is the name of the task {answer}')
        
        self.next_state = self.group
        
    def group(self, answer):
        print(f'this is the group of the task {answer}')

        self.next_state = self.side

    def side(self, answer):
        print(f'this is the side of the task {answer}')

        self.next_state = self.end
        
    def end(self, _):
        pass

    def error(self, _):
        logger.warning('not handelt state')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)


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

    dp.add_handler(MessageHandler(Filters.regex('^[a-zA-Z0-9]'), ca.handle_answer))
    #dp.add_handler(MessageHandler(Filters.text, ca.interpret_text))
    dp.add_handler(CommandHandler('help', error))

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
