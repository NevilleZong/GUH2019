"""
Scheduling management center for obtaining various requests
"""
import importlib
import re
from datetime import datetime
from datetime import timedelta
from auto_reply_bee.utils import config
# from auto_reply_bee.control.horoscope.xzw_horescope import get_today_horoscope


__all__ = ['BOT_NAME_DICT']

BOT_NAME_DICT = {
    1: 'tuling123', 2: 'tian_robot'
}


def get_bot_info(message, userId=''):
    # interact with the robot

    channel = config.get('auto_reply_info').get('bot_channel', 2)
    source = BOT_NAME_DICT.get(channel, 'tian_robot')
    # print(source)
    if source:
        addon = importlib.import_module('auto_reply_bee.control.bot.' + source, __package__)
        reply_msg = addon.get_auto_reply(message, userId)
        return reply_msg

    return None
