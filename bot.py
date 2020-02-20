#!/usr/bin/env python

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

from sql import sql_Connector

class Conv_automat():
    def __init__(self, state_list, cube_exists):
        self.state_dict = {}

        self.state_glob = None

        # mape each state name to the state object:
        for state in state_list:
            self.state_dict[state.state_methode.__name__] = state

        self.cube_exists = cube_exists

        self.last_state = None
        #TODO: catch index error:
        self.curr_state = state_list[0]
        self.next_state = None # will be set by the current methode

        # if more questions are required to get all attributs to create a new object:
        self.curr_builder = None

    def handle_answer(self, update, context):
        """this is the method which handles the state changes"""

        answer = update.message.text

        # here the function has to return the next_state in a dict:
        return_dict = self.curr_state.state_methode(answer, {'return_again':self.state_glob})


        if 'next_state' not in return_dict:
            # TODO: handel errors better
            raise Exception('can not handle answer: no next state defined')
        if 'reply' in return_dict and return_dict['reply']:
            update.message.reply_text(return_dict['reply'])
            

        state_name = return_dict['next_state']

        if state_name not in self.state_dict:
            raise Exception('Not handelt state')

        before = self.state_dict[state_name].pre_enter

        self.next_state = self.state_dict[state_name]

        reply = None
        if isinstance(before, str):
            reply = before
        elif callable(before):
            reply = before({'return_again':self.state_glob})
        elif before == None:
            jump = update
            jump.message.text = None
            context.dispatcher.process_update(jump)
        else:
            raise Exception('Not handelt return value')

        if reply:
            update.message.reply_text(reply)

        logger.debug(f'reply massage for user: {reply}')

        self.last_state = self.curr_state
        self.curr_state = self.next_state
        # the state object will have to set this, based of the users answer or her desision:
        self.next_state = None

        logger.debug(f'changed state to {self.curr_state}')

class State():
    def __init__(self, pre_enter, state_methode):
        self.pre_enter = pre_enter
        self.state_methode = state_methode


class Builder():
    def __init__(self, to_build):
        self.to_build = to_build
        self.argument_list = [None] * self.to_build.__code__.co_argcount
    def build(self):
        return self.to_build(*self.argument_list)
