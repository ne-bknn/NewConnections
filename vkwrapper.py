import vk_api
import os
from cache import FileCache, DummyCache
import sys
import getpass
from typing import List
import time
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Vk:
    def __init__(self, cache = DummyCache(), login: str = "", password: str = ""):
        def tfa_handler():
            code = input("[!] 2fa detected! please enter the code you've just received: ")
            return code, 0

        def _auth(login, password, tfa=tfa_handler):
            session = vk_api.VkApi(login=login,
                               password=password,
                               auth_handler=tfa)

            session.auth()
            vk = session.get_api()
            if vk.users.get(user_ids='1')[0]['id'] == 1:
                log.info("[+] Auth succeeded!")
                return vk
            else:
                log.info("[-] Some error occured")
                sys.exit()
        
        if login == "" or password == "":
            login = input("[?] Enter your login: ")
            password = getpass.getpass("[?] Enter your password: ")

        vk = _auth(login, password)

        self.s = vk
        self.c = cache

    def get_friends(self, target: str) -> List[str]:
        if self.c.contains(target):
            friends = self.c.get(target)
            log.debug("[+] Found {} in cache".format(target))
        else:
            log.debug("[-] Not found {} in cache".format(target))
            try:
                friends = self.s.friends.get(user_id=target)["items"]
            except vk_api.exceptions.ApiError:
                print(f"[!] ID {target} is private. Skipping")
                friends = [] 
        
            self.c.add(target, friends)
    
        friends = [str(friend) for friend in friends]

        return friends

