# coding=utf-8
"""
Program run entry
"""

import sys
import re
from datetime import datetime

# try:
#     from auto_reply_bee import __version__
#
#     print('EverydayWechat Program version：{}'.format(__version__))
#     _date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print('Current time：{}'.format(_date))
# except Exception as exception:
#     print(str(exception))
#     print('Please put the script in the project root directory to run.')
#     print('Please check for the existence of file everyday_wechat')
#     exit(1)


def run():

    # Check for python 3
    if sys.version_info[0] == 2:
        print('We need python 3！')
        return

    # Check if install everything needed
    try:
        import itchat
        import apscheduler
        import requests
        from bs4 import BeautifulSoup
        if itchat.__version__ != '1.3.10':
            print('The version of itchat is：{} , this project needs itchat 1.3.10!\n')
            return

    except (ModuleNotFoundError, ImportError) as error:
        if isinstance(error, ModuleNotFoundError):
            no_modules = re.findall(r"named '(.*?)'$", str(error))
            if no_modules:
                print('Current environment lacks of {} '.format(no_modules[0]))
            print(str(error))
        elif isinstance(error, ImportError):
            print('The current runtime environment has an error with importing the library.')
            print(str(error))
        return


    print('All environment configurations ready ~ ')
    from auto_reply_bee import main
    main.run()


if __name__ == '__main__':
    run()
