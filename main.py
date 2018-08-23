# -*- coding: utf-8 -*-

import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from time import sleep

def captcha_handler(captcha):

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)


def main():
    with open('config.json', 'r', encoding='utf-8') as cfg:
        config = json.load(cfg)

    login, password = config['login'], config['password']
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)

    try:
        vk_session.auth(token_only=True)
        print('You have been connected')
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longPool = VkLongPoll(vk_session)
    print('Poolling is starting')
    for event in longPool.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                print('New message')
                api = vk_session.get_api()
                api.messages.send(user_id = event.user_id, message = config['message'])
                print('Message has been sent')
                sleep(3)

if __name__ == '__main__':
    main()