# -*- coding: utf-8 -*-

import sys
import platform
import requests
from bs4 import BeautifulSoup
import Session

class Entry():
    """Base class for all entries from zhihu"""

    def __init__(self, session, url):
        self.__url = url
        self.__session = session
        self.__rsp = None

        self.soup = None # protected member for specified use

        if self.__getContent():
            self.soup = self.__parse()
        else:
            print "Get url failure!"
            sys.exit(0)

    def __getContent(self):
        try:
            self.__rsp = self.__session.get(self.__url)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if self.__rsp.status_code == requests.codes.ok:
                return True
            else:
                print r.json()['msg']
        return False
    
    def __parse(self):
        return BeautifulSoup(self.__rsp.content)

    def decode2Character(self, content): # protected en/de API
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content