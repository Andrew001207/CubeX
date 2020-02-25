#!/usr/bin/env python

import logging

from cubeX import CubeX
from userX import UserX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Conv_automat:
    
    def __init__(self):
        self.states = self._init_states()

        self.cubeX = None
        self.userX = UserX("Paula")

        #temporary attributes for state collaboration
        self.result_function = None
        self.answers = []

        #TODO: catch index error:
        self.curr_state = "start"
        self.next_state = None # will be set by the current methode

    def handle_answer(self, update, context):
        """this is the method which handles the state changes"""

        answer = update.message.text

        state_method = self.states[self.curr_state][1]

        # call method of current state, return name of next state and optional instant reply
        return_dict = state_method(answer)
        logger.debug(f'called method "{state_method.__name__}"')



        if 'next_state' not in return_dict:
            # TODO: handel errors better
            raise Exception('can not handle answer: no next state defined')
        if 'reply' in return_dict and return_dict['reply']:
            update.message.reply_text(return_dict['reply'])


        next_state_name = return_dict['next_state']

        if next_state_name not in self.states:
            raise Exception('Could not handle state, state does not exist')

        next_pre_enter = self.states[next_state_name][0]

        self.next_state = self.states[next_state_name]

        pre_state_reply = None
        if isinstance(next_pre_enter, str):
            pre_state_reply = next_pre_enter
        elif next_pre_enter is None:
            #Trigger automatic jump to next state
            self.curr_state = self.next_state
            self.next_state = None
            jump = update
            jump.message.text = ''
            self.handle_answer(jump, context) # recursiv call
            context.dispatcher.process_update(jump)
            if pre_state_reply:
                update.message.reply_text(pre_state_reply)
            return
        else:
            raise Exception('Not handeled return value')

        if pre_state_reply:
            update.message.reply_text(pre_state_reply)

        logger.debug(f'reply massage for user: {pre_state_reply}')

        self.curr_state = self.next_state
        # following state will set this
        self.next_state = None

        logger.debug(f'changed state to {self.states[self.curr_state][1].__name__}') 

        ############################## STATES ######################################

    def _init_states(self):
        states = dict()

        def start(self, answer):
            return _return_dict(answer)
        states["start"] = ('Please select a command, for avaiable commands enter "help"', start)

        def cancel(self, answer):
            self._reset()
            return _return_dict("start", "Command cancelled")
        states["cancel"] = (None, cancel)

        def _error(self, update, answer):
            self._reset()
            return _return_dict("start", "Error occurred, trying to start over...")
        states["error"] = (None, _error)

        def create_task(self, answer):
            self.result_function = self.cubeX.create_task
            #Task name conventions?
            self.answers.append(answer)
            return _return_dict("select_group")
        states["create_task"] = ("Please enter the name for the new task", create_task)

        def _create_group(self, answer):
            self.answers.append(answer)
            return _return_dict("optional_add_cube")
        states["create_group"] = ("Please enter the name for the new group", _create_group)

        def _optional_add_cube(self, answer):
            if answer == "skip":
                self.answers.append(None)
            else:
                valid_answer = False if not answer.isdigit() else int(answer) in self.user.list_cubes()
                if valid_answer:
                    self.answers.append(int(answer))
                    ############ EXECUTE DB FUNCTION ################
                    self._execute_function()
                    return _return_dict("start", f"Following task was created: {self.answers}")
                else:
                    return _return_dict("optional_add_cube", "Invalid answer, please try again.")
        states["optional_add_cube"] = ("Select a cube the task should be bound to or enter 'skip'", _optional_add_cube)

        def select_cube(self, answer):
            valid_answer = False if not answer.isdigit() else int(answer) in self.user.list_cubes()
            if valid_answer:
                self.cubeX = CubeX(int(answer))
                if self.result_function:
                    return _return_dict("select_task")
                else:
                    return _return_dict("start", f"Selcted cube {answer}")
            else:
                return _return_dict("select_cube", f"Cube {answer} does not exist, please try again")
        states["select_cube"] = (f"Please enter the ID of the cube you want to select from "\
                                  "the following:\n{self.userX.list_cubes()}", select_cube)

        def _select_task(self, answer):
            #Check if answer is an existing task_id
            valid_answer = False if not answer.isdigit() else int(answer) in [task[0] for task in self.user.list_tasks(self.cubeX.get_cube_id())]
            if valid_answer:
                self.answers.append(int(answer))
                return _return_dict("select_side")
            else:
                return _return_dict("select_task", f"Task {answer} does not exist, please try again")
        states["select_task"] = (f"Please enter the ID of the task you want to select out of the following:"\
                                  "\n(ID, Name, Group), {self.userX.list_tasks(self.cubeX.get_cube_id())}", _select_task)

        def _select_group(self, answer):
            if(answer == "create_group"):
                return _return_dict("create_group")
            else:
                valid_answer = False if not self.user.list_groups() else answer in self.user.list_groups()
                if valid_answer:
                    self.answers.append(answer)
                    return _return_dict("optional_add_cube")
                else:
                    return _return_dict("select_group", f"Group {answer} does not exist, please try again")
        states["select_group"] = (f"Please enter the name of the group you want to select from the following or enter "\
                                   "create_group to create a new one\n{self.userX.list_groups()}", _select_group)

        def _select_side(self, answer):
            valid_answer = False if not answer.isdigit() else int(answer) in range(1, 7)
            if valid_answer:
                self.answers.append(answer)
                ###################### EXECUTE DB FUNCTION #####################
                self._execute_function() #Answer???
                return _return_dict("start")
            else:
                return _return_dict("select_side", f"Side {answer} does not exist, please try again")
        states["select_side"] = ("Please enter the number of the side you want to select", _select_side)

        def map_task(self, answer):
            if self.cubeX:
                self.result_function = self.cubeX.set_task
                return _return_dict("select_task")
            else:
                return _return_dict("select_cube")
        states["map_task"] = (None, map_task)

        #Has to be last to cover all states in help text
        def help(self, answer):
            #TODO add help text
            return _return_dict("start", 'help text')
        states["help"] = (None, help)

        def _return_dict(next_state, reply=None):
            return {
                "next_state": next_state,
                "reply": reply
            }

        return states

    def _reset(self):
        self.result_function = None
        self.answers = []

    def _execute_function(self):
        #TODO Error handling
        self.result_function(*self.answers)
        self._reset()