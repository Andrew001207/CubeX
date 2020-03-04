#!/usr/bin/env python

import logging
import traceback

from cube_api.cubeX import CubeX
from cube_api.userX import UserX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class ConvMachine:
    """This object handles the conversation with the user within telegram

    Note: 
        naming conventions for the states:
            -state name starts with _ if the state cannot be accessed directly by the user (= is not a command)
            -if possible state ends with the by its function affected object (e.g. select_cube, create_task, select_group)
            -if a state is there to set an optional value, it starts with optional or _optional (e.g. _optional_add_cube)
            -if pre-enter shows the user a list to select from and an empty list is allowed, the pre-enter must contain 
             the word "or" (e.g. see _optional_add_cube, _select_group)
    
    Attributes:
        states (dict): The states of the state machine with name as key and tuple of the state' s function, its pre_enter 
                       message and a description of the state
        cubeX (CubeX): Representation of the currently used Smart Cube
        userX (userX): Representation of the database user account
        username (str): Database username
        result_function (function): Function from cube_api which should process the current commands user input
        answers (dict): Stores all the user's answers for the current command
        curr_state (str): The current state of the state machine
        next_state (str): The next state of the state machine
        return_state (str): Used when a necessary precondition to enter a state is not fullfilled. Stores the actual state so that 
                            the states responsible to fullfill this precondition are executed can finally return to the right state
    """

    def __init__(self, username):

        self.states = dict()

        self.cubeX = None
        self.userX = UserX(username)
        self.username = username

        #temporary attributes for state collaboration
        self.result_function = None
        self.answers = dict()

        #TODO: catch index error:
        self.curr_state = "start"

        self.next_state = None # will be set by the current methode

        self.return_state = None

        self._init_states()


    def handle_answer(self, update, context):
        """this is the method which handles the state changes"""
        #TODO handel error
        answer = update.message.text

        #Enable instant start of conversation by telegram bot start
        if answer == "/start":
            answer = "start"

        if answer == "cancel":
            self.curr_state = "cancel"

        self._execute_curr_state(answer, update.message.reply_text)
        self._prepare_next_state(update, context)


    def _execute_curr_state(self, answer, reply_funct):
        """Handle the user's answer with the current state"""

        # get state payload
        state_method = self.states[self.curr_state][1]

        # call method of current state, returns name of next state and optional instant reply
        return_dict = state_method(self, answer)
        logger.debug('called method "%s"', state_method.__name__)

        if 'next_state' not in return_dict:
            # TODO: handel errors better
            raise Exception('can not handle answer: no next state defined')
        if 'reply' in return_dict and return_dict['reply']:
            reply_funct(return_dict['reply'])

        self._set_next_state(return_dict['next_state'])


    def _set_next_state(self, next_state):
        """Update the next state attribute"""
        if next_state in self.states:
            self.next_state = next_state
        else:
            raise Exception(f'Could not handle state {next_state}, state does not exist')


    def _prepare_next_state(self, update, context):
        """Prepare the automat for the next state/answer"""

        next_pre_enter = self.states[self.next_state][0]
        next_pre_enter_reply = None

        instant_next = False

        # get the pre_enter string of next state
        if isinstance(next_pre_enter, str):
            next_pre_enter_reply = next_pre_enter
        elif callable(next_pre_enter):
            # list of formattable string as first element followed by format arguments
            next_pre_enter_args = next_pre_enter(self)
            logger.debug('called method "%s"', next_pre_enter.__name__)

            format_args = next_pre_enter_args[1:]
            next_state_split = list(filter(None, self.next_state.split('_')))

            # if user should select element from empty list
            if [] in format_args and not "or" in next_pre_enter_args[0].split():
                logger.debug('Could not enter state "%s" because cannot select from empty list', self.next_state)
                next_pre_enter_reply = f"No {next_state_split[-1]} to select from, please add one first"
                self.next_state = "cancel"
                instant_next = True
            else:
                next_pre_enter_reply = next_pre_enter_args[0].format(*format_args)
        elif next_pre_enter is None:
            instant_next = True
        else:
            raise Exception('Not handeled return value')

        if next_pre_enter_reply:
            update.message.reply_text(next_pre_enter_reply)

        logger.debug('reply massage for user: %s', next_pre_enter_reply)

        if instant_next:
            self._instant_next_state(update, context)
            return

        self._update_states()


    def _update_states(self):
        """Update state attributes for next state/answer"""
        self.curr_state = self.next_state
        self.next_state = None

        logger.debug('changed state to %s', self.states[self.curr_state][1].__name__)


    def _instant_next_state(self, update, context):
        """Called when the next state should be entered without user input"""
        self._update_states()
        jump = update
        jump.message.text = ''
        self.handle_answer(jump, context)


    def _init_states(self):
        """Setup all states"""


        def _add_to_states(self, function, pre_enter=None, description=None):
            """Add a state to the automat

            Parameters:
                function (function): function to process the user input for the added state
                pre_enter (str or callable which returns list with str and format args): 
                instruction to tell the user, what he should
                input for this state to process as an answer
                description (str): description for the state if user can acces state by command
            """
            self.states[function.__name__] = (pre_enter, function, description)


        def start(self, answer):
            """State function for the start state which processes the commands input by the user"""
            valid_answer = _validate_answer(answer,
                [key for key in self.states.keys() if not key.startswith("_")])
            if valid_answer:
                return _return_dict(answer)

            return _return_dict("start", f"Command '{answer}' does not exist, please try again.")

        _add_to_states(self, start, 'Please select a command, for avaiable commands enter "help"',
            "Start interaction with the bot")


        def help(self, answer):
            """State function to give the user a list of all available commands and their description"""
            help_text = []
            for state in self.states.keys():
                if not state.startswith("_"):
                    help_text.append(f"{state} | {self.states[state][2]}")
            return _return_dict("start", "\n".join(help_text))

        _add_to_states(self, help, description="See availabe commands")


        def cancel(self, answer):
            """State function to cancel and return to start at any time"""

            return _reset_and_start(self, "Command cancelled")

        _add_to_states(self, cancel, description="Cancel any command at any time and return to start")


        def _error(self, update, answer):
            """Internal state function for occurring errors"""
            return _reset_and_start(self, "Error occurred, trying to start over...")

        _add_to_states(self, _error)


        def create_task(self, answer):
            """State function to create a new task"""
            self.result_function = self.userX.create_task
            #Task name conventions?
            return _add_answer_and_continue(self, answer, "task_name", "_select_group")

        _add_to_states(self, create_task, "Please enter the name for the new task",
            "Create a new task for your cubes")


        def delete_task(self, answer):
            """State function to delete a task"""
            valid_answer = _validate_answer(answer,
                [task[0] for task in self.userX.list_tasks(self.cubeX.get_cube_id())], int)
            if valid_answer:
                self.userX.delete_task(valid_answer)
                return _reset_and_start(self, f"Deleted task {answer}")

            return _return_dict("delete_task", "Entered task does not exist, please try again.")

        _add_to_states(self, delete_task,
            lambda self: ["Please enter the ID of the task you want to delete from the following:"\
            "\n{}", self.userX.list_tasks()], "Delete a task")


        def _create_group(self, answer):
            """Internal state function to create a new group for another command"""
            #Group name conventions?
            return _add_answer_and_continue(self, answer, "group_name", "_optional_add_cube")

        _add_to_states(self, _create_group, "Please enter the name for the new group")


        def _optional_add_cube(self, answer):
            """Internal state function to optionally select a cube for another command"""
            if answer == "skip":
                ############ EXECUTE DB FUNCTION ################
                return self._execute_function()

            valid_answer = _validate_answer(answer, self.userX.list_cubes(), int)
            if valid_answer:
                return _add_answer_and_continue(self, answer, "cube_id")

            return _return_dict("_optional_add_cube", "Invalid answer, please try again.")

        _add_to_states(self, _optional_add_cube, lambda self:
            ["Select a cube the task should be bound from the following "\
            "to or enter 'skip'\n{}", self.userX.list_cubes()])


        def select_cube(self, answer):
            """State function to select the cube the user wants to work with"""
            valid_answer = _validate_answer(answer, self.userX.list_cubes(), int)
            if valid_answer:
                self.cubeX = CubeX(valid_answer)
                if self.return_state:
                    self.result_function = self.cubeX.set_task
                    return _return_to_return_state()

                return _return_dict("start", f"Selcted cube {answer}")

            return _return_dict("select_cube", f"Cube '{answer}' does not exist, please try again")

        _add_to_states(self, select_cube,
            lambda self: ["Please enter the ID of the cube you want to select from "\
            "the following:\n{}", self.userX.list_cubes()],
            "Select the cube you want to perform commands on")


        def _select_task(self, answer):
            """Internal state function to select a task for another command"""
            #Check if answer is an existing task_id
            valid_answer = _validate_answer(answer,
                [task[0] for task in self.userX.list_tasks(self.cubeX.get_cube_id())], int)
            if valid_answer:
                return _add_answer_and_continue(self, answer, "task_id", "_select_side")

            return _return_dict("_select_task", f"Task '{answer}' does not exist, please try again")

        _add_to_states(self, _select_task,
            lambda self: ["Please enter the ID of the task you want to select out of the following:"\
            "\n(ID, Name, Group), {}", self.userX.list_tasks(self.cubeX.get_cube_id())])


        def _select_group(self, answer):
            """Internal state function to select a group
            or initiate creating a new group for another command"""
            if answer == "create_group":
                return _return_dict("_create_group")

            valid_answer = _validate_answer(answer, self.userX.list_groups())
            if valid_answer:
                return _add_answer_and_continue(self, answer, "group_name", "_optional_add_cube")

            return _return_dict("_select_group", f"Group '{answer}' does not exist, please try again")

        _add_to_states(self, _select_group,
            lambda self: ["Please enter the name of the group you want to select from the following "\
            "or enter create_group to create a new one\n{}", self.userX.list_groups()])


        def _select_side(self, answer):
            """Internal state function to select a side of the selected cube for another command"""
            valid_answer = _validate_answer(answer, list(range(0, 6)), int)
            if not valid_answer is None:
                return _add_answer_and_continue(self, answer, "side_id")

            return _return_dict("_select_side", f"Side '{answer}' does not exist, please try again")

        _add_to_states(self, _select_side, "Please enter the number of the side you want to select")


        def map_task(self, answer):
            """State function to set a task on a side of the selected cube,
            if no cube is selected, user will be asked to do so"""
            if self.cubeX:
                self.result_function = self.cubeX.set_task
                return _return_dict("_select_task")

            self.return_state = map_task.__name__
            return _return_dict("select_cube", "No cube selected yet...")

        _add_to_states(self, map_task,
            description="Map a task to a side of the currently selected cube, "\
            "if no cube is selected yet, you will be asked to do so")


        def show_cubes(self, answer):
            """State function to list all cubes associated with the user"""
            return _reset_and_start(self, f"You have these cubes:\n{self.userX.list_cubes()}")

        _add_to_states(self, show_cubes, description="List all of your cubes")


        def show_tasks(self, answer):
            """State function to list all tasks created by the user"""
            return _reset_and_start(self, f"You have these tasks:\n{self.userX.list_tasks()}")

        _add_to_states(self, show_tasks, description="List all of your tasks")


        def show_sides(self, answer):
            """State function to list side-task mapping of selected cube"""
            if self.cubeX:
                return _reset_and_start(self,
                    f"The sides of the current cube are mapped like this:\n{self.cubeX.get_side_tasks()}")

            self.return_state = show_sides.__name__
            return _return_dict("select_cube", "No cube selected yet...")

        _add_to_states(self, show_sides,
            description="List all sides and mapped tasks of the currently selected cube")


        def _validate_answer(answer, list_of_valids, cast_funct=None):
            """ Check if answer is valid

            Parameters:
                answer (str): user input
                list_of_valids (list): list with acceptable answers
                cast_funct (function): function with which the answer should casted
                    to the right type, None if string is the expected type

            Returns:
                answer in correct type if in list_of_valids, otherwise None
            """
            final_answer = answer
            if cast_funct:
                try:
                    final_answer = cast_funct(answer)
                except:
                    return None
            if final_answer in list_of_valids:
                return final_answer

            return None


        def _add_answer_and_continue(self, answer, answer_key, next_state=None):
            """
            Parameters:
                answer: user's answer in the needed data type
                answer_key: dictionary position of the answer
                next_state: next state for the automat or
                    None if there is no more user input needed for the command

            Returns:
                dictionary with the next state for the state machine (automat)
                or the result of the commands internal function
            """
            self.answers[answer_key] = answer
            if next_state:
                return _return_dict(next_state)

            return self._execute_function()


        def _reset_and_start(self, reply):
            """Starts the automat over when returned"""
            self._reset()
            return _return_dict("start", reply)


        def _return_dict(next_state, reply=None):
            """Returns a dictionary with given parameters for handle_answer function"""

            return {
                "next_state": next_state,
                "reply": reply
            }


        def _return_to_return_state():
            """
            Return to and reset return_state

            Returns:
                dictionary with next state
            """
            tmp = self.return_state
            self.return_state = None
            return _return_dict(tmp)


    def _reset(self):
        """Reset temporary attributes for new command"""
        self.result_function = None
        self.answers = dict()


    def _execute_function(self):
        """Call the selected userX or cubeX function with the user's input
           to interact with the cube and/or database"""
        try:
            self.result_function(**self.answers)
            return dict(next_state="start",
                reply=f"Sucessfully executed {self.result_function.__name__} with arguments {self.answers}")

        except Exception:
            logger.warning("Error in _execute_function while trying to call %s:\n%s",
                self.result_function.__name__, traceback.format_exc())
            return dict(next_state="_error", reply="Something went wrong")

        self._reset()
