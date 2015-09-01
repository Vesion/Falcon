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

class Column():
    """ Tool class for getting column info. """

    @check_eid
    def __init__(self, session, eid):

        self.session = session
        self.__zhost = self.session.getHeader()['host']
        self.session.setHeader({'host' : "zhuanlan.zhihu.com"})

        self.eid = eid
        self.url = Column_URL + self.eid

        self.json = self.session.get(Columns_Json_URL + self.eid).json()

    def get_name(self):
        return self.json['name']

    def __del__(self):
        self.session.setHeader({'host' : self.__zhost})
        print 'del column obj'
