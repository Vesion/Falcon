# -*- coding: utf-8 -*-

import sys
import platform
import requests
from bs4 import BeautifulSoup
import Session

class Entry():
    """Base class for all specified entries"""

    HOST = "http://www.zhihu.com"

    def __init__(self, session, url):
        self.__rsp = None

        # protected member for specified use
        self.session = session
        self.url = url
        self.soup = None

        # unique identity of each entry
        # always a sequence of number defined by zhihu
        # usually used to locate the web page
        self.Eid = self.url.split('/')[-1]

        if self.__getContent():
            self.soup = self.__parse()
            #with open("web.html", 'wb') as fff:
            #    fff.write(self.soup.text.decode('utf-8').encode('gbk'))
            #print self.decode2Character(self.soup.text.encode('utf-8').strip('\n'))
        else:
            print "Get url failed!"

    def __getContent(self):
        try:
            self.__rsp = self.session.get(Entry.HOST + self.url)
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
        return self.Eid

    # encode/decode character tool API
    def decode2Character(self, content):
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content