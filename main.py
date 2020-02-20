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

def generate_stats():

    state_list = []
    
    def error(update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)

    def select_cube(self, answer):
        if self.cube_exists(int(answer)):
            self.next_state = self.name
        else:
            self.next_state = self.select_cube
        
    def _pre_map_task(self, answer):

        
    def map_task(self, answer):

                self.select_cube:'Please insert your cube id',
                self.side:'please choose a side of the cube',
                self.name:'give the task a name: ',
                self.group:'give the task a group: ',
                self.end : 'task creation finished!',
                'error':self.error

    def start(self, answer):
        """this is a method which handles the answer and changes the state"""

        if answer.lower().strip == 'help':
            self.next_state = self.help
        # set here the following state
        self.next_state = self.select_cube

    start = State('Please select a command, for avaiable commands enter "help"', start)
    state_list.append(start)

    def name(self, answer):
        """this is a method which handles the answer and changes the state"""
        print(f'this is the name of the task {answer}')

        self.next_state = self.group

    def group(self, answer):
        """this is a method which handles the answer and changes the state"""
        print(f'this is the group of the task {answer}')

        self.next_state = self.side

    def side(self, answer):
        """this is a method which handles the answer and changes the state"""
        print(f'this is the side of the task {answer}')

        self.next_state = self.end_create_task

    def end_create_task(self, _):
        pass

    def error(self, _):
        logger.warning('not handelt state')


    return state_list
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)
    #TODO: check token

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # create a instanc of the conversation automat:
    ca = Conv_automat(generate_states(), bot_token)

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
