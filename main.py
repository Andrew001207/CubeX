import logging, traceback

from telegram.ext import Updater, MessageHandler, Filters

from config_aware import ConfigAware

from conv_automat import Conv_automat
from userX import UserX
from cubeX import CubeX
#from cubeX import CubeX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


logger.info('Read config')

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
    ca = Conv_automat()

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
