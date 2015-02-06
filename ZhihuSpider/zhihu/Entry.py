# -*- coding: utf-8 -*-

import sys
import platform
from bs4 import BeautifulSoup
import Session

class Entry():
    """Base class for all entries from zhihu"""

    def __init__(self, session, url):
        self.url = url
        self.session = session
        self.soup = self.__parse(self.__getContent(self.url))

    def __getContent(self, url):
        return self.session.get(url)
    
    def __parse(self, rsp):
        return BeautifulSoup(rsp.content)

    def decode2Chinese(self, content):
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content