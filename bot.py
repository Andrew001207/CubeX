#!/usr/bin/env python

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class Conv_automat():
    def __init__(self):
        #self.last_state = None
        self.curr_state = self.start
        self.next_state = None # will be set by the current methode

        # mape here you functions to the question or statments,
        # which you would like to send to the User,
        # BEFOR your function will be called with the answer,
        # or mape your function to a function with returns a string for the user
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

    def start(self, answer):

        # set here the following state
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


