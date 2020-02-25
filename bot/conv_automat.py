#!/usr/bin/env python

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Conv_automat():
    def __init__(self, state_list, cube_exists):
        self.state_dict = {}

        # mape each state name to the state object:
        for state in state_list:
            self.state_dict[state.state_methode.__name__] = state

        #TODO: catch index error:
        self.curr_state = state_list[0]
        self.next_state = None # will be set by the current methode

        # if more questions are required to get all attributs to create a new object:
        self.curr_builder = None

    def handle_answer(self, update, context):
        """this is the method which handles the state changes"""


        answer = update.message.text

        # here the function has to return the next_state in a dict:
        return_dict = self.curr_state.state_methode(answer, {'return_again':self.again_return})
        self.again_return = return_dict['return_again']
        logger.debug(f'called method "{self.curr_state.state_methode.__name__}"')



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
            reply = before({'return_again':self.again_return})
            logger.debug(f'called method "{before.__name__}"')
        elif before is None:
            self.last_state = self.curr_state
            self.curr_state = self.next_state
            self.next_state = None
            jump = update
            jump.message.text = ''
            self.handle_answer(jump, context) # recursiv call
            context.dispatcher.process_update(jump)
            if reply:
                update.message.reply_text(reply)
            return
        # the state object will have to set this, based of the users answer or her desision:
        else:
            raise Exception('Not handelt return value')

        if reply:
            update.message.reply_text(reply)

        logger.debug(f'reply massage for user: {reply}')

        self.last_state = self.curr_state
        self.curr_state = self.next_state
        # the state object will have to set this, based of the users answer or her desision:
        self.next_state = None

        logger.debug(f'changed state to {self.curr_state.state_methode.__name__}') 

        ############################## STATES ######################################

        def _init_states(self):
            states = {
                "direct": {}
                "indirect": {}
            }

            def _start(self, answer):
            """this is a method which handles the answer and changes the state"""
            #TODO: implement me!
                return _return_dict(answer)
            state_list.append('Please select a command, for avaiable commands enter "help"', start))

            def _help(self, answer):
                return _return_dict("start", 'help text')
            state_list.append(State(None, help))

            def _cancel(self, answer):
                #TODO Clear builder
                return _return_dict("start", "Command cancelled")
            state_list.append(State(None, cancel))

            def _error(self, update, answer):
                """Log Errors caused by Updates."""
                return _return_dict("start", "Error occurred, trying to start over...")
            state_list.append(State(None, error))

            def _create_task(self, answer):
                return _return_dict("select_group", answers=["answer"], result_function=arg_dict["cubeX"].create_Task)
            state_list.append(State("Please enter the name for the new task", create_task))

            def _create_group(self, answer):
                #TODO call db method
                if arg_dict["result_function"].__name__ == "create_Task":
                    arg_dict["answers"].append(answer)
                    return _return_dict("optional_add_cube", f"Following group was created: {answer}")

                return _return_dict("error", "How the hell did you do this???")

            state_list.append(State("Please enter the name for the new group", create_group))

            def _optional_add_cube(self, answer):
                if answer == "skip":
                    arg_dict["answers"].append(None)
                else:
                    valid_answer = False if not answer.isdigit() else int(answer) in UserX(user).list_cubes()
                    if valid_answer:
                        arg_dict["answers"].append(int(answer))
                    return _return_dict("optional_add_cube", "Invalid answer, please try again.")
                ############ EXECUTE DB FUNCTION ################
                arg_dict["result_function"](*arg_dict["answers"])
                return _return_dict("start", f"Following task was created: {arg_dict['answers']}")
            state_list.append(State("Select a cube the task should be bound to or enter 'skip'", optional_add_cube))

            def _select_cube(self, answer):
                #Replace true with DB method cube exists
                valid_answer = False if not answer.isdigit() else int(answer) in UserX(user).list_cubes()
                if valid_answer:
                    cubeX = CubeX(int(answer))
                    if "result_function" in arg_dict:
                        return _return_dict("select_task", result_function=cubeX.setTask, cubeX=cubeX, answers=[], **arg_dict)
                    return _return_dict("start", f"Selcted cube {answer}", cubeX=cubeX)
                return _return_dict("select_cube", f"Cube {answer} does not exist, please try again")
            state_list.append(State(f"Please enter the ID of the cube you want to select from the following:\n{UserX(user).list_cubes()}", select_cube))

            def _select_task(self, answer):
                """this is a method which handles the answer and changes the state"""
                #Replace true with DB method task exists
                if "result_function" in arg_dict:
                    valid_answer = False if not answer.isdigit() else int(answer) in UserX(user).list_tasks(arg_dict["cubeX"].get_cube_id()) #TODO only cmp with ids
                    if valid_answer:
                        arg_dict["answers"].append(int(answer))
                        return _return_dict("select_side", **arg_dict)
                    return _return_dict("select_task", f"Task {answer} does not exist, please try again")
                return _return_dict("error", f"How the hell did you do this???")

            state_list.append(State(lambda arg_dict: f"Please enter the ID of the task you want to select out of the following:\n(ID, Name, Group), {UserX(user).list_tasks(arg_dict['cubeX'].get_cube_id())}", select_task))

            def _select_group(self, answer):
                """this is a method which handles the answer and changes the state"""
                #Replace true with DB method group exists
                if(answer == "create_group"):
                    return _return_dict("create_group", **arg_dict)
                else:
                    if "result_function" in arg_dict:
                        valid_answer = False if not UserX(user).list_groups() else answer in UserX(user).list_groups()
                        if valid_answer:
                            if arg_dict["result_function"].__name__ == "create_Task":
                                arg_dict["answers"].append(answer)
                                return _return_dict("optional_add_cube", **arg_dict)
                            return _return_dict("error", f"How the hell did you do this???")
                        return _return_dict("select_group", f"Group {answer} does not exist, please try again")
                    return _return_dict("error", f"How the hell did you do this???")
            state_list.append(State("Please enter the name of the group you want to select or enter create_group to create a new one", select_group))

            def _select_side(self, answer):
                #Replace true with DB method group exists
                if "result_function" in arg_dict:
                    valid_answer = False if not answer.isdigit() else int(answer) in range(1, 7)
                    if valid_answer:
                        arg_dict["answers"].append(answer)
                        ########## EXECUTE DB FUNCTION #####################
                        try:
                            build_result = arg_dict["result_function"](*arg_dict["answers"])
                            if not build_result:
                                logger.warning(f"Function {arg_dict['result_function'].__name__} called from function select_side did not work")
                                _return_dict("error", "Something went wrong")
                        except Exception:
                            logger.warning(f"Failed to execute funtion {arg_dict['result_function'].__name__} from function select_side with error\n{traceback.format_exc()}")
                            return _return_dict("error", "Something went wrong")
                    return _return_dict("start") #Any answer from builder instead of None
                elif False and "result_function" in arg_dict:
                    return _return_dict("select_side", f"Side {answer} does not exist, please try again")
                return _return_dict("error", f"How the hell did you do this???")
            state_list.append(State("Please enter the number of the side you want to select", select_side))

            def _map_task(self, answer):
                #TODO DB function map_task instead of none
                if "cubeX" in arg_dict:
                    return _return_dict("select_task", result_function=arg_dict["cubeX"].setTask, answers=[], **arg_dict)
                return _return_dict("select_cube", "No cube selected yet", result_function="TODO To be set", **arg_dict)
            state_list.append(State(None, map_task))