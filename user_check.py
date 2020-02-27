#!/usr/bin/env python

import logging

from telegram.ext.precheckoutqueryhandler import PreCheckoutQueryHandler
from sql.sql_Connector import SqlConn
from conv_automat import Conv_automat

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class UserCheck(PreCheckoutQueryHandler):


    def __init__(self, callback):
        self.user_conv_handlers = {}

    def check_update(self, update):
        """Determines whether an update should be passed to this handlers :attr:`callback`.

        Args:
            update (:class:`telegram.Update`): Incoming telegram update.

        Returns:
            :obj:`bool`

        """
        if not update.message:
            #TODO:
            raise Exception('no message to be processed')

        tel_id = update.message.from_user.id
        # TODO: other name? :
        # NOTE: added lower because the database is not consisent with the case:
        user_first_name = update.message.from_user.first_name.lower()

        if tel_id in self.user_conv_handlers:
            # NOTE: PAIN!
            self.callback = self.user_conv_handlers[tel_id].handle_answer
            return True

        conn = SqlConn()
        if conn.is_telegram_id_user(tel_id):
            self.user_conv_handlers[tel_id] = Conv_automat(user_first_name)
            # NOTE: PAIN!
            self.callback = self.user_conv_handlers[tel_id].handle_answer
            return True

        try:
            # TODO: catch duplicated name in db
            # TODO: implement password conv_handler
            conn.signup_user(user_first_name, '', telegram_id=tel_id)
        except Exception:
            conn.set_telegram_user(user_first_name, tel_id)
        self.user_conv_handlers[tel_id] = Conv_automat(user_first_name)
        # NOTE: PAIN!
        self.callback = self.user_conv_handlers[tel_id].handle_answer
        return True
