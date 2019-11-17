"""
Handle messages from friends
"""

import time
import random
import itchat
# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os

from auto_reply_bee.utils import config
from auto_reply_bee.utils.data_collection import (
    get_bot_info
)
from auto_reply_bee.utils.common import (
    FILEHELPER
)


__all__ = ['handle_friend']

def handle_friend(msg):
    try:

        # Ignore message sent from phone.
        if msg['FromUserName'] == config.get('wechat_uuid') and msg['ToUserName'] != FILEHELPER:
            return

        conf = config.get('auto_reply_info')
        if not conf.get('is_auto_reply'):
            return
        # Get the sender id.
        uuid = FILEHELPER if msg['ToUserName'] == FILEHELPER else msg['FromUserName']
        is_all = conf.get('is_auto_reply_all')
        auto_uuids = conf.get('auto_reply_black_uuids') if is_all else conf.get('auto_reply_white_uuids')
        # Ignore users in black list when reply to all mode is turned on.
        if is_all and uuid in auto_uuids:
            return

        # When not in reply to all mode and the user is not in white list, ignore.
        if not is_all and uuid not in auto_uuids:
            return

        receive_text = msg.text  # Message content sent by friends.
        nick_name = FILEHELPER if uuid == FILEHELPER else msg.user.nickName       
        print('\n{} sent message：{}'.format(nick_name, receive_text))
        words = receive_text.split()

        if (words[0].lower() == "/tts"):
            if (len(words) == 1):
                reply_text = "Please provide at least one word to convert to speech."
                time.sleep(random.randint(1, 2))  # Sleep for one second.

                prefix = conf.get('auto_reply_prefix', '')
                if prefix:
                    reply_text = '{}{}'.format(prefix, reply_text)

                suffix = conf.get('auto_reply_suffix', '')
                if suffix:
                    reply_text = '{}{}'.format(reply_text, suffix)

                itchat.send(reply_text, toUserName=uuid)
                print('Replied by {}：{}'.format(nick_name, reply_text))
            else:
                (firstWord, rest) = receive_text.split(maxsplit=1)
                itchat.send("You're in 'text to speech' mode. Converting your text.", toUserName=uuid)
                mytext = rest
                # Language in which you want to convert
                language = 'en'

                # Passing the text and language to the engine,
                # here we have marked slow=False. Which tells
                # the module that the converted audio should
                # have a high speed
                myobj = gTTS(text=mytext, lang=language, slow=False)

                # Saving the converted audio in a mp3 file named
                # welcome
                myobj.save("textToSpeech.mp3")

                time.sleep(random.randint(1, 2))
                print('MP3 sending')
                itchat.send("Please wait patiently.", toUserName=uuid)
                reply = itchat.send_file('textToSpeech.mp3', toUserName=uuid)
                print(reply['BaseResponse']['ErrMsg'])
                print('MP3 sent')
                
        else:
            # Future modification to fix possible bug
            if (words[0].lower() == "sing"):
                reply_text = "send_music_command"

            elif (words[0].lower() == "hi"):
                reply_text = "send_hi_command"
            else:
                reply_text = get_bot_info(receive_text, uuid)  # Get auto reply
            
            if (reply_text == "send_music_command"):
                time.sleep(random.randint(1, 2))
                print('MP3 sending')
                itchat.send("Singing now, please wait patiently.", toUserName=uuid)
                reply = itchat.send_file('music.mp3', toUserName=uuid)
                print(reply['BaseResponse']['ErrMsg'])
                print('MP3 sent')

            elif (reply_text == "send_hi_command"):
                time.sleep(random.randint(1, 2))
                print('Image sending')
                reply_text = "Hi. Sending you cute bee gif."

                prefix = conf.get('auto_reply_prefix', '')
                if prefix:
                    reply_text = '{}{}'.format(prefix, reply_text)

                suffix = conf.get('auto_reply_suffix', '')
                if suffix:
                    reply_text = '{}{}'.format(reply_text, suffix)

                itchat.send(reply_text, toUserName=uuid)
                print('Replied by {}：{}'.format(nick_name, reply_text))
                reply = itchat.send_image('bee.gif', toUserName=uuid)
                print(reply['BaseResponse']['ErrMsg'])
                print('Image sent') 
            
            elif reply_text:  # If content is not empty, reply.
                time.sleep(random.randint(1, 2))  # Sleep for one second.

                prefix = conf.get('auto_reply_prefix', '')
                if prefix:
                    reply_text = '{}{}'.format(prefix, reply_text)

                suffix = conf.get('auto_reply_suffix', '')
                if suffix:
                    reply_text = '{}{}'.format(reply_text, suffix)

                itchat.send(reply_text, toUserName=uuid)
                print('Replied by {}：{}'.format(nick_name, reply_text))
            else:
                print('Fail to auto reply\n')
    except Exception as exception:
        print(str(exception))
