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

from util import myconversationhandler, mystarthandler
import logging, configparser
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#NOTE: is there a nicer way than global?
curr_cube_id = None
conv_state_fact = 0

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

def get_select_cube_conv(update, context, return_state=ConversationHandler.END):

    def process_results(answers):
        """Update selected cube"""
        global curr_cube_id
        curr_cube_id = answers[0]
        print("ID set")

    return  [create_conv_handler(update, context, [], process_results, return_state, "Enter Cube_ID"), "Enter Cube_ID"]
    
def select_cube(update, context):
    """Select currently used Cube"""
    get_handler = get_select_cube_conv(update, context)
    start_conversation(update, context, get_handler[0], get_handler[1])

def get_map_task_conv(update, context):

    def process_results(answers):
        """Update selected cube"""
        pass
        # global curr_cube_id
        # task_name = answers[0]
        # cube_side = answers[1]
        # print(f'Mapped task {task_name} onto side {cube_side} for cube {curr_cube_id}.')
        #Actual processing

    my_args = ["Please insert the name of the task", "Please insert the number of the side of the cube"]

    if not curr_cube_id:
        inner_handler = get_select_cube_conv(update, context, 1)
        my_args[0:0] = ["No Cube selected yet...", inner_handler[0]]
        print("Args: ", my_args)

    return  [create_conv_handler(update, context, my_args[1:], process_results), my_args[0]]

def map_task(update, context):
    """Map a given Task to a Side of the current Cube """
    get_handler = get_map_task_conv(update, context)
    start_conversation(update, context, get_handler[0], get_handler[1])

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update with id: "%s" caused error "%s"', update['update_id'], context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1082890355:AAH4pPdvhLHfxnvimffZgdiIJPL3_BDrd9w', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # command to map task
    dp.add_handler(CommandHandler("mt", map_task))
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

def create_conv_handler(update, context, questions, process_results=lambda answers: None, return_state=MyConversationHandler.END, sr=""):
    """Creates and returns a ConversationHandler asking the User the given questions"""
    answers = [] #Save Useres answers

    #Store and clear handlery temporaryly
    handlers_tmp = context.dispatcher.handlers[0]

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
        set_handlers(context, handlers_tmp)
        print("State End")
        return MyConversationHandler.END

    def i_wrong_input(update, context):
        update.message.reply_text("Wrong input, command stopped.")
        set_handlers(context, handlers_tmp)
        return MyConversationHandler.END

    conv_handlers = [] #Handlers for each state of the ConversationHandler

    ###################
    if questions and isinstance(questions[0], MyConversationHandler):
        tmp = questions.pop(0)
        conv_handlers.append([tmp])

    for i in range(len(questions)):

        def i_ask_answer_funtion(update, context):
            """
            Funtion to store Useres last answer and ask the next question

            Returns:
            Next state for the ConversationHandler
            """
            answers.append(update.message.text)
            update.message.reply_text(questions[i])
            print(f"New State {i+1}")
            return i+1
        
        conv_handlers.append([MessageHandler(Filters.regex('^[0-9a-zA-Z]'), i_ask_answer_funtion), MessageHandler(Filters.all, i_wrong_input)])

    conv_handlers.append([MessageHandler(Filters.regex('^[0-9a-zA-Z]'), i_end), MessageHandler(Filters.all, i_wrong_input)])

    print("States: ", dict(zip(range(len(questions)+1), conv_handlers)))

    #Create actual ConversationHandler
    conv_handler = MyConversationHandler(
        sr,

        states=dict(zip(range(len(questions)+1), conv_handlers)), #Map each handler to the numbers 0..x

        fallbacks=[MessageHandler(Filters.command, i_wrong_input)],

        map_to_parent={MyConversationHandler.END: return_state}
    )

    return conv_handler

def start_conversation(update, context, conv_handler):

    def i_start(bot, update):
        """
        Entry function for ConversationHandler asking the User the first question
        
        Returns:
        First state of the ConversationHandler for next question
        """
        update.message.reply_text(initial_response)
        print("New State 0")
        return 0

    #Add handler temporaryly to current dispatcher
    set_handlers(context, [conv_handler])

    #Autostart ConversationHandler
    #conv_handler.handle_update(update, context.dispatcher, (conv_handler._get_key(update), MessageHandler(Filters.regex('^$'), i_start),re.match('^$','')))

def set_handlers(context, handlers):
    context.dispatcher.handlers[0] = []
    any(context.dispatcher.add_handler(handler) for handler in handlers)

################################################### Helpers End ######################################################   


if __name__ == '__main__':
    main()
