# coding=utf-8

"""
core code
"""

import platform
import os
from apscheduler.schedulers.background import BackgroundScheduler
import itchat
from itchat.content import (
    TEXT
)
from everyday_wechat.utils.data_collection import (
    get_dictum_info,
    get_constellation_info
)
from everyday_wechat.utils import config
from everyday_wechat.utils.itchat_helper import (
    init_wechat_config,
    set_system_notice
)
from everyday_wechat.utils.group_helper import (
    handle_group_helper
)
from everyday_wechat.utils.friend_helper import (
    handle_friend
)


__all__ = ['run', 'delete_cache']


def run():
    # Check if login successfully.
    # If not, then login automatically.
    # If returned value is false, then it means fail to login.
    print('Login...')
    if not is_online(auto_login=True):
        print('Logout...')
        return


def is_online(auto_login=False):
    def _online():
        # Get friends' information to check if the user is still online.
        try:
            if itchat.search_friends():
                return True
        except IndexError:
            return False
        return True

    if _online(): return True  # If the user is online, return True.
    if not auto_login:  # If not, return False
        print('Offline..')
        return False

    # hotReload = not config.get('is_forced_switch', False)  # Switch to a different account, requiring to scan QR code again.
    hotReload = False  # Have to scan QR code to login everytime.
    loginCallback = init_data
    exitCallback = exit_msg
    try:
        for _ in range(2):  # Try to login for a second time.
            if platform.system() in ('Windows', 'Darwin'):
                itchat.auto_login(hotReload=hotReload,
                                  loginCallback=loginCallback, exitCallback=exitCallback)
                itchat.run(blockThread=True)
            else:
                # Show QR code on the terminal.
                itchat.auto_login(enableCmdQR=2, hotReload=hotReload, loginCallback=loginCallback,
                                  exitCallback=exitCallback)
                itchat.run(blockThread=True)
            if _online():
                print('Successful!')
                return True
    except Exception as exception:  # Handle login failures
        failure = str(exception)
        if failure == "'User'":
            print('Cannot apply this account to online WeChat. Please try with a different account.')
        else:
            print(failure)

    delete_cache()  # Clean up cached data
    print('Fail to login')
    return False


def delete_cache():
    # Clear cached data, in case they show next time.
    file_names = ('QR.png', 'itchat.pkl')
    for file_name in file_names:
        if os.path.exists(file_name):
            os.remove(file_name)


def init_data():
    # Initialise all the data needed.
    set_system_notice('Login successfully')
    itchat.get_friends(update=True)  # Update friends data
    itchat.get_chatrooms(update=True)  # Update group chat information

    init_wechat_config()  # Initialize all the configuration content


@itchat.msg_register([TEXT])
def text_reply(msg):
    """ Track friends' messages for auto reply """
    handle_friend(msg)


@itchat.msg_register([TEXT], isGroupChat=True)
def text_group(msg):
    """ Track groups' messages for auto reply """
    handle_group_helper(msg)


def exit_msg():
    """ Exit notice """
    print('The program has quit.')

