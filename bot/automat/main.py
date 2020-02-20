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

    start = State('Please select a command, for avaiable commands enter "help"', start)
    state_list.append(start)

    #########################################################################################

    def start(self, answer, **kwargs):
        """this is a method which handles the answer and changes the state"""
        return _return_dict(answer, None)
        # next_states = {
        #     'help': self.help
        #     'select_cube': 
        # }

    def help(self, answer, **kwargs):

    def cancel(self, answer, **kwargs):
    
    def error(update, answer, **kwargs):
        """Log Errors caused by Updates."""
        logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)

    def create_task(self, answer, **kwargs):
        #TODO call db method
        return _return_dict("start", f"Following task was created: {answer}")

    def create_group(self, answer, **kwargs):
        #TODO call db method
        return _return_dict("start", f"Following group was created: {answer}")

    def select_cube(self, answer, **kwargs):
        #Replace true with DB method cube exists
        if True and "builder" in kwargs:
            return _return_dict("select_task", None)
        elif True and not "builder" in kwargs:
            return _return_dict("start", f"Selcted cube {answer}")
        else:
            return _return_dict("select_cube", f"Cube {answer} does not exist, please try again")

    def select_task(self, answer, **kwargs):
        """this is a method which handles the answer and changes the state"""
        #Replace true with DB method task exists
        if True and "builder" in kwargs:
            return _return_dict("select_group", None) 
        elif False and "builder" in kwargs:
            return _return_dict("select_task", f"Task {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")

    def select_group(self, answer, **kwargs):
        """this is a method which handles the answer and changes the state"""
        #Replace true with DB method group exists
        if True and "builder" in kwargs:
            return _return_dict("select_side", None)
        elif False and "builder" in kwargs:
            return _return_dict("select_group", f"Group {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")

    def select_side(self, answer, **kwargs):
        #Replace true with DB method group exists
        if True and "builder" in kwargs:
            builder.build()
            return _return_dict("start", None) #Any answer from builder instead of None
        elif False and "builder" in kwargs:
            return _return_dict("select_side", f"Side {answer} does not exist, please try again")
        else:
            return _return_dict("error", f"How the hell did you do this???")

    def map_task(self, answer, **kwargs):
        #TODO create builder
        if #cube set?:
            _return_dict("select_task", None)
        else:
            _return_dict("select_cube", "No cube selected yet")

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
