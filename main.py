import logging, traceback

from telegram.ext import Updater, MessageHandler, Filters

from config_aware import ConfigAware

from bot import State, Conv_automat
from userX import UserX
from cubeX import CubeX
#from cubeX import CubeX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


logger.info('Read config')

user = "Paula"

def _init_states():

    state_list = []

    def _start(self, answer):
        """this is a method which handles the answer and changes the state"""
        #TODO: implement me!
        return _return_dict(answer)
    state_list.append(State('Please select a command, for avaiable commands enter "help"', start))

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

    return state_list

def _return_dict(next_state, reply=None, **self_return):
    return {
        "next_state": next_state,
        "reply": reply,
        "return_again": self_return
    }

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)

def main(bot_token):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)
    #TODO: check token

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # create a instanc of the conversation automat:
    ca = Conv_automat(_init_states(), bot_token)

    dp.add_handler(MessageHandler(Filters.regex('^[a-zA-Z0-9]'), ca.handle_answer))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    conf = ConfigAware()
    main(conf.conf_bot_token)
