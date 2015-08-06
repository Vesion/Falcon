#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

import platform

from .Utils import *
from .Session import Session

class Entry():
    """
    Base class for all specified entries.
    An entry is identified by a unique url, like '/question/27936593'
    the only way to instantiate an entry is getting by url.
    NOTE:
        All of get_* APIs in tool classes are NOT getting an entry,
        but getting text|url|urllist|dict, for performance regrading.
        (Use that Entry(session, url) to manually get an entry instance indeed)
    API: encode2Character
    Wrapper: getContent, getSoup, getId
    """

    def __init__(self, session, url = ""):

        # after login, request session is maitained automatically
        self.session = session

        # unique identity of each entry
        # like '/question/27936593'
        self.url = url

        # get the soup after getting content
        # IF url not provided, get homepage entry
        self.soup = self.getSoup(self.getContent(HOST_URL + self.url))

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

    # encode Chinese characters
    def encode2Character(self, content):
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content
        
