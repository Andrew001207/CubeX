#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, configparser
import re, automat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler


#NOTE: is there a nicer way than global?
curr_cube_id = None

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

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


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""

    update.message.reply_text("""You can use the following commands:
    /help - See available commands
    /ct - Create a new task
    /sc - Select a cube""")
    
def select_cube(update, context):
    """Select currently used Cube"""

    def process_results(answers):
        """Update selected cube"""
        curr_cube_id = answers[0]

    start_conversation(update, context, ["Enter Cube_ID"], process_results)


def create_task(update, context):
    """Create a new task for the cube"""
    start_conversation(update, context, ["Enter name"])


def map_task_conv(update, context):
    """Map a given Task to a Side of the current Cube """
    if not curr_cube_id:
        #TODO: make command_names not hardcoded:
        # command_name = command_dict['select_cube']
        start_conversation(update, context, ['No Cube selected, please run the command "\\sc"'])
        return
    
    def process_results(answers):
        """Update selected cube"""
        task_name = answers[0]
        cube_side = answers[1]
        _map_task(curr_cube_id, task_name, cube_side)

    start_conversation(update, context, ["Please insert the name of the task", "Please insert the number of the side of the cube"])

def _map_task(cube, task, side):
    #TODO: map task to side of cube
    pass



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)

class Conv_automat():
    _machine = automat.MethodicalMachine()

    def __init__(self, parent=None):
        self.state = 'start'
        self.parent = parent
        self.answer = None

    @_machine.state()
    def got_name(self):
        '''got a name form user'''
        print('got a name')

    @_machine.state()
    def got_group(self):
        print('got group')

    @_machine.input()
    def input(self):

    @_machine.input()
    def interpret_text(self):
        #self.answer = update.message.text

    @_machine.output()
    def _process_answer(self, answer):
        self._process_answer(update.message.text)


    @_machine.input()
    def interpret_command(self, answer):
        
    @_machine.state()
    def end(self):
        pass


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # create a instanc of the conversation automat:
    ca = Conv_automat()
    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(Filters.regex('^[a-zA-Z0-9]'), ca.interpret_text)
    dp.add_handler(CommandHandler(Filters.regex('^[a-zA-Z0-9]'), ca.interpret_command)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # command to create new task
    dp.add_handler(CommandHandler("ct", create_task))

    # command to select current cube
    dp.add_handler(CommandHandler("sc", select_cube))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


 ###################################################### Helpers #######################################################

def start_conversation(update, context, questions, process_results=lambda answers: None):
    """Creates and returns a ConversationHandler asking the User the given questions"""
    answers = [] #Save Useres answers

    #Store and clear handlery temporaryly
    handlers_tmp = context.dispatcher.handlers[0]
    
    def i_start(bot, update):
        """
        Entry function for ConversationHandler asking the User the first question
        
        Returns:
        First state of the ConversationHandler for next question
        """
        update.message.reply_text(questions[0])
        return 0

    def i_end(update, context):
        """
        Final function for the ConversationHandler processing the Users whole input and clearing up the handlers

        Returns:
        End state for the ConversationHandler to stop
        """
        answers.append(update.message.text)
        process_results(answers)
        update.message.reply_text(f'Answers: {str(answers)}')
        #Reset handlers
        restore_handlers(context, handlers_tmp)
        return ConversationHandler.END

    def i_wrong_input(update, context):
        update.message.reply_text("Wrong input, command stopped.")
        restore_handlers(context, handlers_tmp)
        return ConversationHandler.END

    conv_handlers = [] #Handlers for each state of the ConversationHandler

    for i in range(len(questions)-1):

        def i_ask_answer_funtion(update, context):
            """
            Funtion to store Useres last answer and ask the next question

            Returns:
            Next state for the ConversationHandler
            """
            answers.append(update.message.text)
            update.message.reply_text(questions[i+1])
            return i+1
        
        conv_handlers.append([MessageHandler(Filters.regex('^[0-9a-zA-Z]'), i_ask_answer_funtion), MessageHandler(Filters.all, i_wrong_input)])

    conv_handlers.append([MessageHandler(Filters.regex('^[0-9a-zA-Z]'), i_end), MessageHandler(Filters.all, i_wrong_input)])

    #Create actual ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[], #Starts automated

        states=dict(zip(range(len(questions)), conv_handlers)), #Map each handler to the numbers 0..x

        fallbacks=[MessageHandler(Filters.command, i_wrong_input)]
    )

    #Add handler temporaryly to current dispatcher
    set_single_handler(context, conv_handler)

    #Autostart ConversationHandler
    conv_handler.handle_update(update, context.dispatcher, (conv_handler._get_key(update), MessageHandler(Filters.regex('^$'), i_start),re.match('^$','')))

def set_single_handler(context, handler):
    context.dispatcher.handlers[0] = []
    context.dispatcher.add_handler(handler)

def restore_handlers(context, old_handlers):
    context.dispatcher.handlers[0] = []
    any(context.dispatcher.add_handler(handler) for handler in old_handlers)

################################################### Helpers End ######################################################   


if __name__ == '__main__':
    main()
