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
        but getting text/url/urllist/dict, for performance regrading.
        (Use that Entry(session, url) to manually get an entry instance indeed)
    API: encode2Character
    Wrapper: getContent, getSoup, getId
    """

    def __init__(self, session, url = ''):

        # protected member for specific use
        self.session = session
        self.soup = None

        # unique identity of each entry
        # always a sequence of number defined by zhihu
        # usually used to locate the web page
        self.url = url

        self.soup = self.getSoup(self.getContent(Session._HOST_ + self.url))

    def getContent(self, url):
        try:
            rsp = self.session.get(url)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            if rsp.status_code == requests.codes.ok:
                return rsp.content
        return None
    
    def getSoup(self, content):
        return BeautifulSoup(content)

    def getId(self):
        return self.url.split('/')[-1]

    # encode/decode character tool API
    def encode2Character(self, content):
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content
        