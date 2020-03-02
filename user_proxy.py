#!/usr/bin/env python

import logging

from telegram.ext.handler import Handler
from sql.sql_Connector import SqlConn
from conv_automat import Conv_automat

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class UserProxy(Handler):
    '''A handler missused as a proxy,
    to send the updates to the conversation automat of the user
    depending on the user id'''

    def __init__(self, callback):
        self.user_conv_handlers = {}
        # TODO: set self.callback allways to None?
        self.callback = callback

    def check_update(self, update):
        """determents to which user the update should be send

        Args:
            update (:class:`telegram.Update`): Incoming telegram update.

        Returns:
            :obj:`bool`

        """
        if not update.message:
            #TODO:
            raise Exception('no message to be processed')

        tel_id = update.message.from_user.id
        # NOTE: added lower because the database is not consisent with the case:
        user_first_name = update.message.from_user.first_name.lower()

        if tel_id in self.user_conv_handlers:
            self.callback = self.user_conv_handlers[tel_id].handle_answer
            return True

        conn = SqlConn()
        if conn.is_telegram_id_user(tel_id):
            self.user_conv_handlers[tel_id] = Conv_automat(user_first_name)
            self.callback = self.user_conv_handlers[tel_id].handle_answer
            return True
        # TODO: redirect user to signup on website
        self.callback = self._unknown_user
        return True

    def _unknown_user(self, update, context):
        'callback function if the users telegram id is not known to the database'
        update.message.reply_text('It seems like an error occured or your telegram id is not known to us.')

