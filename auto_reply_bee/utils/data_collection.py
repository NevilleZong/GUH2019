"""
Scheduling management center for obtaining various requests
"""
import importlib
import re
from datetime import datetime
from datetime import timedelta
from everyday_wechat.utils import config
from everyday_wechat.control.horoscope.xzw_horescope import get_today_horoscope


__all__ = ['BOT_NAME_DICT']

BOT_NAME_DICT = {
    1: 'tuling123', 3: 'qingyunke', 4: 'qq_nlpchat',
    5: 'tian_robot', 6: 'ruyiai', 7: 'ownthink_robot'
}


def get_bot_info(message, userId=''):
    # interact with the robot

    channel = config.get('auto_reply_info').get('bot_channel', 7)
    source = BOT_NAME_DICT.get(channel, 'ownthink_robot')
    # print(source)
    if source:
        addon = importlib.import_module('everyday_wechat.control.bot.' + source, __package__)
        reply_msg = addon.get_auto_reply(message, userId)
        return reply_msg

    return None

