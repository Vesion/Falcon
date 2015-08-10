#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

from .Utils import *
from .Session import Session

class Entry():
    """
    Base class for all specified entries.
    An entry is identified by a unique eid(entry-id), like '/question/27936593'.
    NOTE:
        All of get_* APIs in tool classes are NOT getting an entry,
        but getting text|eid|eidlist|dict, for performance regrading.
        Use that Entry(session, eid) to manually get an entry instance indeed
    API: encode2Character
    Wrapper: getContent, getSoup
    """

    def __init__(self, session, eid = ''):

        # after login, request session is maitained automatically
        self.session = session

        # get the entire url with host and entry id
        self.url = HOST_URL + eid

        # get the soup after getting content
        # IF url not provided, get homepage entry
        self.soup = self.getSoup(self.getContent(self.url))

    def getContent(self, url):
        try:
            rsp = self.session.get(url)
        except requests.exceptions.RequestException as e:
            print e.message()
        else:
            return rsp.content
        return None
    
    def getSoup(self, content):
        return BeautifulSoup(content)

    # encode Chinese characters
    # discarded!
    def encode2Character(self, content):
        if platform.system() == "Windows":
            content = content.decode('utf-8').encode('gbk')
        return content
