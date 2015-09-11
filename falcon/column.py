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

    def get_description(self):
        return self.json['description']

    def get_creator(self):
        return '/people/{0}'.format(self.json['creator']['profileUrl'].split('/')[-1])

    def get_num_followers(self):
        return self.json['followersCount']

    def get_num_posts(self):
        return self.json['postsCount']

    def get_posts(self):
        num = self.get_num_posts()
        params = {'limit' : num, 'offset' : 0}
        posts = self.session.get(Columns_Json_URL + self.eid + "/posts", params = params).json()
        for post in posts:
            yield post['url']

    def get_all_posts(self):
        return get_all_(self.get_posts)

    def __del__(self):
        self.session.setHeader({'host' : self.__zhost})
        print 'del column obj'
