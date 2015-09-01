#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

from .utils import *
from .session import Session

class Entry():
    """
    Base class for all specified entries.
    An entry is identified by a unique eid(entry-id), like '/question/27936593'.
    All of get_* APIs in tool classes are NOT getting an entry,
    but getting text|eid|eidlist|dict, for performance regrading.
    Use that Entry(session, eid) to manually get an entry content indeed
    Wrapper: getContent, getSoup
    """

    @check_eid
    def __init__(self, session, eid = ''):

        # after login, request session is maitained automatically
        self.session = session

        # get the entire url with host and entry id
        self.eid = eid
        self.url = HOST_URL + self.eid

        # get the soup after getting content
        # IF url not provided, get homepage entry
        self.soup = self.getSoup(self.getContent(self.url))

    def getContent(self, url):
        rsp = self.session.get(url)
        if rsp.status_code == requests.codes.ok:
            return rsp.content
        else:
            sys.exit("Get entry failed: {0}".format(rsp.status_code)) 
    
    def getSoup(self, content):
        return BeautifulSoup(content)
