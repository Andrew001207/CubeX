import traceback, logging, configparser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot import State, Conv_automat, Builder
from cubeX import CubeX
# Read configfile
config = configparser.ConfigParser()

config_filename = ".bot.conf"
config.read(config_filename)

username = input('please insert your username: ')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


try:
    bot_token = config[username]['token']
except KeyError:
    bot_token = input('''please insert you token from Botfather or create a ~/CubeX/Bots/.bot.conf file like this
[<username>]
token=<token>
and insert your username and token ther
''')

logger.info('Read config')

def init_states():

    state_list = []

    def start(self, answer, arg_dict, **kwargs):
        """this is a method which handles the answer and changes the state"""
        return _return_dict(answer)
    state_list.append(State('Please select a command, for avaiable commands enter "help"', start))

    def help(self, answer, arg_dict, **kwargs):
        return _return_dict("start")
    state_list.append(State('help text', help))

    def cancel(self, answer, arg_dict, **kwargs):
        #TODO Clear builder
        return _return_dict("start")
    state_list.append(State("Command cancelled", cancel))

    def error(update, answer, arg_dict, **kwargs):
        """Log Errors caused by Updates."""
        return _return_dict("start")

    def create_task(self, answer, arg_dict, **kwargs):
        #TODO call db method
        return _return_dict("start", f"Following task was created: {answer}")
    state_list.append(State("Please enter the name for the new task", create_task))

    def create_group(self, answer, arg_dict, **kwargs):
        #TODO call db method
        return _return_dict("start", f"Following group was created: {answer}")
    state_list.append(State("Please enter the name for the new group", create_group))

    def select_cube(self, answer, arg_dict, **kwargs):
        #Replace true with DB method cube exists
        if True and kwargs['builder']:
            cubeX = CubeX(answer)
            return _return_dict("select_task", builder=Builder(cubeX.setTask), cubeX=cubeX)
        elif True and kwargs['builder']:
            return _return_dict("start", f"Selcted cube {answer}")
        else:
            return _return_dict("select_cube", f"Cube {answer} does not exist, please try again")
    state_list.append(State("Please enter the ID of the cube you want to select", select_cube))

    def select_task(self, answer, arg_dict, **kwargs):
        """this is a method which handles the answer and changes the state"""
        #Replace true with DB method task exists
        if True and "builder" in kwargs:
            return _return_dict("select_group", None)
        elif False and "builder" in kwargs:
            return _return_dict("select_task", f"Task {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")
    state_list.append(State("Please enter the name of the task you want to select", select_task))

    def select_group(self, answer, arg_dict, **kwargs):
        """this is a method which handles the answer and changes the state"""
        #Replace true with DB method group exists
        if True and "builder" in kwargs:
            return _return_dict("select_side")
        elif False and "builder" in kwargs:
            return _return_dict("select_group", f"Group {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")
    state_list.append(State("Please enter the name of the group you want to select", select_group))

    def select_side(self, answer, arg_dict, **kwargs):
        #Replace true with DB method group exists
        if True and "builder" in kwargs:
            try:
                build_result = kwargs['builder'].build()
            except Exception as e:
                _return_dict("error", "Something went wrong")
            return _return_dict("start", None) #Any answer from builder instead of None
        elif False and "builder" in kwargs:
            return _return_dict("select_side", f"Side {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")
    state_list.append(State("Please enter the number of the side you want to select", select_side))

    def map_task(self, answer, arg_dict, **kwargs):
        #TODO DB function map_task instead of none
        if arg_dict["cubeX"]:
            _return_dict("select_task", None, Builder(arg_dict["cubeX"].set_task))
        else:
            _return_dict("select_cube", "No cube selected yet", "Need to build Builder", **arg_dict)
    state_list.append(State(None, map_task))

    return state_list

def _return_dict(next_state, reply=None, builder=None, **self_return):
    print(type(self_return))
    return {
        "next_state": next_state,
        "reply": reply,
        "builder": builder,
        "return_again": self_return
    }

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
    ca = Conv_automat(init_states(), bot_token)

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
    main(input('please insert your bot token: '))
