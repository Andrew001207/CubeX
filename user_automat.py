#!/usr/bin/env python

import logging

from telegram.ext.precheckoutqueryhandler import PreCheckoutQueryHandler
from cubeX import CubeX
from userX import UserX

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class UserAutomate(PreCheckoutQueryHandler):
    def check_update(self, update):
        """Determines whether an update should be passed to this handlers :attr:`callback`.

        Args:
            update (:class:`telegram.Update`): Incoming telegram update.

        Returns:
            :obj:`bool`

        """
        return isinstance(update, Update) and update.pre_checkout_query

