#!/usr/bin/env python

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

from sql import sql_Connector

class Conv_automat():
    def __init__(self, cube_exists):
        self.cube_exists = cube_exists

        self.last_state = None
        self.curr_state = self.start
        self.next_state = None # will be set by the current methode

        # mape here you functions to the question or statments,
        # which you would like to send to the User,
        # BEFOR your function will be called with the answer,
        # or mape your function to a function with returns a string for the user
        self.state_texts = {
            }

    def handle_answer(self, update, context):
        """this is the method which handles the state changes"""

        answer = update.message.text

        self.curr_state(answer) # here the function has to set the next_state

        try:
            befor = self.state_texts[self.next_state]
        except KeyError as e:
            # befor = self.state_texts['error']
            # TODO: handel errors better
            self.next_state = self.end
            befor = 'an error okkured: keyerror'

        if isinstance(befor, str):
            reply = befor
        #TODO: elif callable(befor):
        else:
            reply = befor()

        update.message.reply_text(reply)

        logger.debug(f'reply massage for user: {reply}')

        self.curr_state = self.next_state
        # the function will have to set this, based of the users answer or her desision:
        self.next_state = None

        logger.debug(f'changed state to {self.curr_state}')

class State():
    def __init__(self, pre_enter, state_methode):
        self.pre_enter = pre_enter
        self.state_methode = state_methode
