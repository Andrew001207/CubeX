#!/usr/bin/env python

import logging, traceback

from cubeX import CubeX
from userX import UserX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Conv_automat:

    def __init__(self):

        self.states = dict()

        self.cubeX = None
        self.userX = UserX("Paula")

        #temporary attributes for state collaboration
        self.result_function = None
        self.answers = dict()

        #TODO: catch index error:
        self.curr_state = "start"
        self.next_state = None # will be set by the current methode

        self._init_states()

    def handle_answer(self, update, context):
        """this is the method which handles the state changes"""
        #TODO handel error
        answer = update.message.text

        state_method = self.states[self.curr_state][1]

        # call method of current state, return name of next state and optional instant reply
        return_dict = state_method(self, answer)
        logger.debug(f'called method "{state_method.__name__}"')

        if 'next_state' not in return_dict:
            # TODO: handel errors better
            raise Exception('can not handle answer: no next state defined')
        if 'reply' in return_dict and return_dict['reply']:
            update.message.reply_text(return_dict['reply'])

        self.next_state = return_dict['next_state']

        if self.next_state not in self.states:
            raise Exception('Could not handle state, state does not exist')

        next_pre_enter = self.states[self.next_state][0]

        pre_state_reply = None
        if isinstance(next_pre_enter, str):
            pre_state_reply = next_pre_enter
        elif callable(next_pre_enter):
            pre_state_reply = next_pre_enter(self)
            logger.debug(f'called method "{next_pre_enter.__name__}"')
        elif next_pre_enter is None:
            #Trigger automatic jump to next state
            self.curr_state = self.next_state
            self.next_state = None
            jump = update
            jump.message.text = ''
            self.handle_answer(jump, context) # recursiv call
            return
        else:
            raise Exception('Not handeled return value')

        if pre_state_reply:
            update.message.reply_text(pre_state_reply)

        logger.debug(f'reply massage for user: {pre_state_reply}')

        self.curr_state = self.next_state
        self.next_state = None

        logger.debug(f'changed state to {self.states[self.curr_state][1].__name__}') 

    def _init_states(self):

        def _add_to_states(self, function, pre_enter=None, description=None):
            self.states[function.__name__] = (pre_enter, function, description)

        def start(self, answer):
            return _return_dict(answer)
        _add_to_states(self, start, 'Please select a command, for avaiable commands enter "help"', "Start interaction with the bot")

        def help(self, answer):
            #TODO add help text
            help_text = []
            for state in self.states.keys():
                if not state.startswith("_"):
                    help_text.append(f"{state} | {self.states[state][2]}")
            return _return_dict("start", "\n".join(help_text))
        _add_to_states(self, help, description="See availabe commands")

        def cancel(self, answer):
            return _reset_and_start(self, "Command cancelled")
        _add_to_states(self, cancel, description="Cancel any command at any time and return to start")

        def _error(self, update, answer):
            return _reset_and_start(self, "Error occurred, trying to start over...")
        _add_to_states(self, _error)

        def create_task(self, answer):
            self.result_function = self.userX.create_task
            #Task name conventions?
            return _add_answer_and_continue(self, answer, "task_name", "select_group")
        _add_to_states(self, create_task, "Please enter the name for the new task", "Create a new task for your cubes")

        def _create_group(self, answer):
            #Group name conventions?
            return _add_answer_and_continue(self, answer, "group_name", "optional_add_cube")
        _add_to_states(self, _create_group, "Please enter the name for the new group")

        def _optional_add_cube(self, answer):
            if answer == "skip":
                ############ EXECUTE DB FUNCTION ################
                return self._execute_function()
            else:
                valid_answer = _validate_answer(answer, self.userX.list_cubes(), int)
                if valid_answer:
                    return _add_answer_and_continue(self, answer, "cube_id")
                else:
                    return _return_dict("optional_add_cube", "Invalid answer, please try again.")
        _add_to_states(self, _optional_add_cube, lambda self: f"Select a cube the task should be bound from the following "\
                                                              f"to or enter 'skip'\n{self.userX.list_cubes()}")

        def select_cube(self, answer):
            valid_answer = _validate_answer(answer, self.userX.list_cubes(), int)
            if valid_answer:
                self.cubeX = CubeX(valid_answer)
                if self.result_function:
                    self.result_function = self.cubeX.set_task
                    return _return_dict("select_task")
                else:
                    return _return_dict("start", f"Selcted cube {answer}")
            else:
                return _return_dict("select_cube", f"Cube {answer} does not exist, please try again")
        _add_to_states(self, select_cube, lambda self: f"Please enter the ID of the cube you want to select from "\
                       f"the following:\n{self.userX.list_cubes()}", "Select the cube you want to perform commands on")

        def _select_task(self, answer):
            #Check if answer is an existing task_id
            valid_answer = _validate_answer(answer, [task[0] for task in self.userX.list_tasks(self.cubeX.get_cube_id())], int)
            if valid_answer:
                return _add_answer_and_continue(self, answer, "task_id", "select_side")
            else:
                return _return_dict("select_task", f"Task {answer} does not exist, please try again")
        _add_to_states(self, _select_task, lambda self: f"Please enter the ID of the task you want to select out of the following:"\
                                                        f"\n(ID, Name, Group), {self.userX.list_tasks(self.cubeX.get_cube_id())}")

        def _select_group(self, answer):
            if(answer == "create_group"):
                return _return_dict("create_group")
            else:
                valid_answer = _validate_answer(answer, self.userX.list_groups())
                if valid_answer:
                    return _add_answer_and_continue(self, answer, "group_name", "optional_add_cube")
                else:
                    return _return_dict("select_group", f"Group {answer} does not exist, please try again")
        _add_to_states(self, _select_group, lambda self: f"Please enter the name of the group you want to select from the following "\
                                                         f"or enter create_group to create a new one\n{self.userX.list_groups()}")

        def _select_side(self, answer):
            valid_answer = _validate_answer(answer, range(1, 7), int)
            if valid_answer:
                return _add_answer_and_continue(self, answer, "side_id")
            else:
                return _return_dict("select_side", f"Side {answer} does not exist, please try again")
        _add_to_states(self, _select_side, "Please enter the number of the side you want to select")

        def map_task(self, answer):
            if self.cubeX:
                self.result_function = self.cubeX.set_task
                return _return_dict("select_task")
            else:
                self.result_function = 'TODO be set'
                return _return_dict("select_cube")
        _add_to_states(self, map_task, description="Map a task to a side of the currently selected cube, "\
                                                   "if no cube is selected yet, you will be asked to do so")

        def _validate_answer(answer, list_of_valids, cast_funct=None):
            final_answer = answer
            if(cast_funct):
                try:
                    final_answer = cast_funct(answer)
                except:
                    return None
            if(final_answer in list_of_valids):
                return final_answer
            else:
                return None

        def _add_answer_and_continue(self, answer, answer_key, next_state=None):
            self.answers[answer_key] = answer
            if(next_state):
                return _return_dict(next_state)
            else:
                return self._execute_function()

        def _reset_and_start(self, reply):
            self._reset()
            return _return_dict("start", reply)

        def _return_dict(next_state, reply=None):
            return {
                "next_state": next_state,
                "reply": reply
            }

    def _reset(self):
        self.result_function = None
        self.answers = dict()

    def _execute_function(self):
        #TODO Error handling and add username
        try:
            self.result_function(**self.answers)
            return dict(next_state="start", reply=f"Sucessfully executed {self.result_function.__name__} with arguments {self.answers}")
        except Exception:
            logger.warning(f"Error in _execute_function while trying to call {self.result_function.__name__}:\n{traceback.format_exc()}")
            return dict(next_state="error", reply="Something went wrong")
        self._reset()
