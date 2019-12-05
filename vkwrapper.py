import vk_api
import os
from cache import FileCache
import sys
import getpass
from typing import List
import time
import logging

c = FileCache()
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def auth():
    def tfa_handler():
        code = input("[!] 2FA detected! Please enter the code you've just received: ")
        return code, 0

    def _auth(login, password, tfa=tfa_handler):
        session = vk_api.VkApi(login=login,
                               password=password,
                               auth_handler=tfa)

        session.auth()
        vk = session.get_api()
        if vk.users.get(user_ids='1')[0]['id'] == 1:
            print("[+] Auth succeeded!")
            return vk
        else:
            print("[-] Some error occured")
            sys.exit()
    
    login = input("[?] Enter your login: ")
    password = getpass.getpass("[?] Enter your password: ")

    vk = _auth(login, password)

    return vk

def get_friends(s, target: str) -> List[int]:
    if c.contains(target):
        friends = c.get(target)
        log.debug("[+] Found {} in cache".format(target))
    else:
        log.debug("[-] Not found {} in cache".format(target))
        try:
            friends = s.friends.get(user_id=target)["items"]
        except vk_api.exception.ApiError:
            print(f"[!] ID {target} is private. Skipping")
            friends = [] 
        
        c.add(target, friends)

    return friends

