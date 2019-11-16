"""
Handle group messages
"""

import re
import itchat
from everyday_wechat.utils import config
from everyday_wechat.utils.data_collection import (
    get_bot_info
)

__all__ = ['handle_group_helper']


def handle_group_helper(msg):
    """
    Handle group messages
    """
    uuid = msg.fromUserName  # group uid
    ated_uuid = msg.actualUserName  # uuid of the user who @ you
    ated_name = msg.actualNickName  # the user's name in the group
    text = msg['Text']  # message sent to the group

    # Do not handle message sent from phone
    if ated_uuid == config.get('wechat_uuid'):
        return

    conf = config.get('group_helper_conf')
    if not conf.get('is_open'):
        return

    # If turn on the mode (only reply to @), then ignore message without @ you 
    if conf.get('is_at') and not msg.isAt:
        return

    is_all = conf.get('is_all', False)
    user_uuids = conf.get('group_black_uuids') if is_all else conf.get('group_white_uuids')
    # If set to reply to all the groups, ignore groups in black list.
    if is_all and uuid in user_uuids:
        return

    # If normal mode, but the group is not in white list, ignore too.
    if not is_all and uuid not in user_uuids:
        return

    # Remove @.
    text = re.sub(at_compile, '', text)

    # If it is help setting.
    helps = re.findall(help_complie, text, re.I)
    if helps:
        retext = help_group_content.format(ated_name=ated_name)
        itchat.send(retext, uuid)
        return

    # Auto reply.
    if conf.get('is_auto_reply'):
        reply_text = get_bot_info(text, ated_uuid)  # Get the automatic reply.
        if reply_text:  # If content is not empty, reply.
            reply_text = common_msg.format(ated_name=ated_name, text=reply_text)
            itchat.send(reply_text, uuid)
            print('Reply{}：{}'.format(ated_name, reply_text))
        else:
            print('Fail to auto reply\n')

