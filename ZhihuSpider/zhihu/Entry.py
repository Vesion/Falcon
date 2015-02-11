# -*- coding: utf-8 -*-

import sys
import platform
import requests
from bs4 import BeautifulSoup
from Session import Session

class Entry():
    """
    Base class for all specified entries.
    Each entry is identified by a unique url, 
    the only way to instantiate an entry is getting by url.
    NOTE:
        All of get_* APIs in tool classes are NOT getting an entry,
        but getting its url, for performance regrading.
        (Use that Entry(session, url) to manually get an entry instance indeed)
    """

    def __init__(self, session, url):

        # protected member for specified use
        self.session = session
        self.soup = None

        # unique identity of each entry
        # always a sequence of number defined by zhihu
        # usually used to locate the web page
        self.url = url

        if self.__getContent():
            print "Get entry content"
        else:
            print "Get entry failed!"

    def __getContent(self):
        # reset the referer of the header
        self.session.setHeader(referer = self.session._HOST_ + self.url)

        try:
            rsp = self.session.get(Session._HOST_ + self.url)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                self.soup = self.getSoup(rsp.content)
                return True
        return False
    
    def getSoup(self, content):
        return BeautifulSoup(content)

    def get_id(self):
        return self.url.split('/')[-1]

    # encode/decode character tool API
    def encode2Character(self, content):
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content