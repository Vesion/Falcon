# -*- coding: utf-8 -*-

import sys
import platform
import requests
from bs4 import BeautifulSoup
import Session

class Entry():
    """Base class for all entries from zhihu"""

    host = "http://www.zhihu.com"

    def __init__(self, session, url):
        self.__rsp = None
        
        self.session = session
        self.url = url
        self.soup = None # protected member for specified use

        if self.__getContent():
            self.soup = self.__parse()
        else:
            print "Get url failure!"
            sys.exit(0)

    def __getContent(self):
        try:
            self.__rsp = self.session.get(Entry.host + self.url)
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

    def get_id(self):
        return self.url.split('/')[-1]

    def decode2Character(self, content): # protected en/de API
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content