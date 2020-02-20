from bot import State, Conv_automat
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

def init_states():

    state_list = []

    def start(self, answer, **kwargs):
        """this is a method which handles the answer and changes the state"""
        return _return_dict(answer, None)
        # next_states = {
        #     'help': self.help
        #     'select_cube': 
        # }
    state_list.append(State('Please select a command, for avaiable commands enter "help"', start))

    def help(self, answer, **kwargs):
        return _return_dict("start", None)
    state_list.append(State('help text', help))

    def cancel(self, answer, **kwargs):
        #TODO Clear builder
        return _return_dict("start", None)
    state_list.append(State("Command cancelled", cancel))
    
    def error(update, answer, **kwargs):
        """Log Errors caused by Updates."""
        logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)

    def create_task(self, answer, **kwargs):
        #TODO call db method
        return _return_dict("start", f"Following task was created: {answer}")
    state_list.append(State("Please enter the name for the new task", create_task))

    def create_group(self, answer, **kwargs):
        #TODO call db method
        return _return_dict("start", f"Following group was created: {answer}")
    state_list.append(State("Please enter the name for the new group", create_group))

    def select_cube(self, answer, **kwargs):
        #Replace true with DB method cube exists
        if True and "builder" in kwargs:
            return _return_dict("select_task", None)
        elif True and not "builder" in kwargs:
            return _return_dict("start", f"Selcted cube {answer}")
        else:
            return _return_dict("select_cube", f"Cube {answer} does not exist, please try again")
    state_list.append(State("Please enter the ID of the cube you want to select", select_cube))

    def select_task(self, answer, **kwargs):
        """this is a method which handles the answer and changes the state"""
        #Replace true with DB method task exists
        if True and "builder" in kwargs:
            return _return_dict("select_group", None) 
        elif False and "builder" in kwargs:
            return _return_dict("select_task", f"Task {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")
    state_list.append(State("Please enter the name of the task you want to select", select_task))

    def select_group(self, answer, **kwargs):
        """this is a method which handles the answer and changes the state"""
        #Replace true with DB method group exists
        if True and "builder" in kwargs:
            return _return_dict("select_side", None)
        elif False and "builder" in kwargs:
            return _return_dict("select_group", f"Group {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")
    state_list.append(State("Please enter the name of the group you want to select", select_group))

    def select_side(self, answer, **kwargs):
        #Replace true with DB method group exists
        if True and "builder" in kwargs:
            builder.build()
            return _return_dict("start", None) #Any answer from builder instead of None
        elif False and "builder" in kwargs:
            return _return_dict("select_side", f"Side {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")
    state_list.append(State("Please enter the number of the side you want to select", select_side))

    def map_task(self, answer, **kwargs):
        #TODO create builder
        if #cube set?:
            _return_dict("select_task", None)
        else:
            _return_dict("select_cube", "No cube selected yet")
    state_list.append(State(None, map_task))

    return state_list

def _return_dict(next_state, reply):
    return {
        "next_state": next_state
        "reply": reply
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
    main(input('please insert your bot token: '))
