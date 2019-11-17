import itchat
import re
from datetime import datetime
from datetime import timedelta
from importlib import import_module
from auto_reply_bee.utils import config
from auto_reply_bee.utils.common import (
    md5_encode,
    FILEHELPER_MARK,
    FILEHELPER
)
from auto_reply_bee.utils.data_collection import (
    BOT_NAME_DICT
)

__all__ = ['init_wechat_config', 'set_system_notice', 'get_group', 'get_friend']

TIME_COMPILE = re.compile(r'^\s*([01]?[0-9]|2[0-3])\s*[：:\-]\s*([0-5]?[0-9])\s*$')


def init_wechat_config():
    """ Initialize the data required for WeChat """
    myset = config.copy()
    print('=' * 80)

    base_wechat_info = itchat.search_friends()  # Get the basic information of this WeChat account.
    wechat_nick_name = base_wechat_info['NickName']  # Get the nickname of this WeChat account.
    wechat_uuid = base_wechat_info['UserName']  # Get the uuid of this WeChat account.
    myset['wechat_nick_name'] = wechat_nick_name
    myset['wechat_uuid'] = wechat_uuid

    #---------------------------Handle auto replying to friends---------------------------start
    reply = myset.get('auto_reply_info')
    if reply is not None and reply.get('is_auto_reply'):
        if reply.get('is_auto_reply_all'):
            auto_reply_list_key = 'auto_reply_black_list'
            auto_reply_list_uuid_name = 'auto_reply_black_uuids'
        else:
            auto_reply_list_key = 'auto_reply_white_list'
            auto_reply_list_uuid_name = 'auto_reply_white_uuids'

        auto_reply_uuids_list = []
        for name in reply.get(auto_reply_list_key):
            if not name.strip():
                continue
            if name.lower() in FILEHELPER_MARK:  # Determine whether the file is transfer assistant.
                auto_reply_uuids_list.append(FILEHELPER)
                continue
            friend = get_friend(name)
            if friend:
                auto_reply_uuids_list.append(friend['UserName'])

        reply[auto_reply_list_uuid_name] = set(auto_reply_uuids_list)

     #---------------------------Handle auto replying to friends---------------------------end


    #-----------------------------------Group function initialization-----------------------------------start
    helper = myset.get('group_helper_conf')
    if helper is not None and helper.get('is_open'):
        if helper.get('is_all', False):
            group_list_key = 'group_name_black_list'
            group_list_uuid_name = 'group_black_uuids'
        else:
            group_list_key = 'group_name_white_list'
            group_list_uuid_name = 'group_white_uuids'
        group_uuid_list = []
        for name in helper.get(group_list_key):
            if not name.strip():
                continue
            group = get_group(name)
            if group:
                group_uuid_list.append(group['UserName'])
            else:
                print('Group Name "{}" is wrong '
                      '(Notice：must save the needed groups into address book)'.format(name))
        helper[group_list_uuid_name] = set(group_uuid_list)

    #-----------------------------------Group function initialization----------------------------------- end

    alarm = myset.get('alarm_info')
    alarm_dict = {}
    if alarm is not None and alarm.get('is_alarm'):
        for gi in alarm.get('girlfriend_infos'):
            ats = gi.get('alarm_timed')
            if not ats:
                continue
            uuid_list = []
            nickname_list = []
            #---------------------------Handle friends---------------------------start
            friends = gi.get('wechat_name')
            if isinstance(friends, str):
                friends = [friends]
            if isinstance(friends, list):
                for name in friends:
                    if name.lower() in FILEHELPER_MARK:  # Determine whether it is file transfer assistant
                        uuid_list.append(FILEHELPER)
                        nickname_list.append(name)
                        continue
                    name_info = get_friend(name)
                    if not name_info:
                        print('Friend nickname"{}" in timed reminder is invalid'.format(name))
                    else:
                        uuid_list.append(name_info['UserName'])
                        nickname_list.append(name)
            #---------------------------Handle friends---------------------------end

            #---------------------------Handle groups---------------------------start
            group_names = gi.get('group_name')
            if isinstance(group_names, str):
                group_names = [group_names]
            if isinstance(group_names, list):
                for name in group_names:
                    name_info = get_group(name)
                    if not name_info:
                        print('Group name "{}" is wrong'.format(name))
                    else:
                        uuid_list.append(name_info['UserName'])
                        nickname_list.append(name)
            #---------------------------Handle groups---------------------------end

            #---------------------------Timing processing---------------------------start

            if isinstance(ats, str):
                ats = [ats]
            if isinstance(ats, list):
                for at in ats:
                    times = TIME_COMPILE.findall(at)
                    if not times:
                        print('Time {} format goes wrong'.format(at))
                        continue
                    hour, minute = int(times[0][0]), int(times[0][1])
                    temp_dict = {'hour': hour, 'minute': minute, 'uuid_list': uuid_list, 'nickname_list': nickname_list}
                    temp_dict.update(gi)
                    alarm_dict[md5_encode(str(temp_dict))] = temp_dict
        #---------------------------Timing processing---------------------------end
        alarm['alarm_dict'] = alarm_dict

    config.update(myset)

    log_all_config()


def set_system_notice(text):
    if text:
        text = 'System notification：' + text
        itchat.send(text, toUserName=FILEHELPER)


def get_group(group_name, update=False):
    if update: itchat.get_chatrooms(update=True)
    if not group_name: return None
    groups = itchat.search_chatrooms(name=group_name)
    if not groups: return None
    return groups[0]


def get_friend(wechat_name, update=False):
    if update: itchat.get_friends(update=True)
    if not wechat_name: return None
    friends = itchat.search_friends(name=wechat_name)
    if not friends: return None
    return friends[0]


def get_mps(mp_name, update=False):
    if update: itchat.get_mps(update=True)
    if not mp_name: return None
    mps = itchat.search_mps(name=mp_name)
    if not mps: return None
    return mps[0]


def log_all_config():
    print('=' * 80)
    channel = config.get('auto_reply_info').get('bot_channel', 7)
    source = BOT_NAME_DICT.get(channel, 'ownthink_robot')
    addon = import_module('auto_reply_bee.control.bot.' + source, __package__)
    bot_name = addon.BOT_NAME
    
    #----------------------------------- Auto reply to friends -----------------------------------start
    reply = config.get('auto_reply_info', None)
    if not reply or not reply.get('is_auto_reply'):
        print('Auto reply is not openned to friends.')
    else:
        if reply.get('is_auto_reply_all'):
            auto_uuids = reply.get('auto_reply_black_uuids')
            nicknames = []
            for auid in auto_uuids:
                if auid == 'filehelper':
                    nicknames.append(auid)
                else:
                    friends = itchat.search_friends(userName=auid)
                    nickname = friends.nickName
                    nicknames.append(nickname)
            nns = '，'.join(nicknames)
            print('Apply auto reply to all the friends, apart from: {}'.format(nns))
        else:
            auto_uuids = reply.get('auto_reply_white_uuids')
            nicknames = []
            for auid in auto_uuids:
                if auid == 'filehelper':
                    nicknames.append(auid)
                else:
                    friends = itchat.search_friends(userName=auid)
                    nickname = friends.nickName
                    nicknames.append(nickname)
            nns = '，'.join(nicknames)
            print('To friend {}, applying auto reply'.format(nns))

    print('=' * 80)

    #----------------------------------- Auto reply to groups -----------------------------------start
    helper = config.get('group_helper_conf')
    if not helper or not helper.get('is_open'):
        print('The group assistant feature is not turned on.')
    else:
        if helper.get('is_all'):
            auto_uuids = helper.get('group_black_uuids')
            nicknames = []
            for auid in auto_uuids:
                chatrooms = itchat.search_chatrooms(userName=auid)
                nickname = chatrooms['NickName']
                nicknames.append(nickname)
            nns = '，'.join(nicknames)
            print('Apply auto reply to groups, apart from: {}。'.format(nns))
        else:
            auto_uuids = helper.get('group_white_uuids')
            nicknames = []
            for auid in auto_uuids:
                chatroom = itchat.search_chatrooms(userName=auid)
                nickname = chatroom['NickName']  # group name
                nicknames.append(nickname)
            nns = '，'.join(nicknames)

            print('Auto reply are now applied to groups：{} '.format(nns))

            if helper.get('is_auto_reply'):
                print('Auto reply to groups has started.')


    print('=' * 80)
