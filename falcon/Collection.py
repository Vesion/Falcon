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
from .Entry import Entry

class Collection(Entry):
    """ Tool class for getting collection info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        """ Return title text. """
        return self.soup.find('h2', id = 'zh-fav-head-title')\
                        .get_text(strip = True).encode(CODE)

    def get_creator(self):
        """ Return creator url. """
        return self.soup.find('h2', class_ = 'zm-list-content-title')\
                        .a['href']
