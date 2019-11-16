"""
Tools
"""

import re
import hashlib
import json

__all__ = ['FILEHELPER_MARK', 'FILEHELPER', 'is_json', 'md5_encode']

FILEHELPER_MARK = ['文件传输助手', 'filehelper']  # File transfer assistant ID
FILEHELPER = 'filehelper'

SPIDER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                  'WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
}


def is_json(resp):
    # Check if data can be Json
    try:
        json.loads(resp.text)
        return True
    except AttributeError as error:
        return False
    return False


def md5_encode(text):
    """ Make data md5 """
    if not isinstance(text, str):
        text = str(text)
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    encodedStr = md5.hexdigest().upper()
    return encodedStr
