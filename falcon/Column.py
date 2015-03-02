# -*- coding: utf-8 -*-

import re

from Entry import Entry

class Column(Entry):
    """ Tool class for getting column info """

    _cHOST_ = "http://zhuanlan.zhihu.com/"

    def __init__(self, session, url):
        self.session = session
        self.url = url

        self.soup = self.getSoup(self.getContent(Column._cHOST_ + self.url))

    def get_title(self):
        title = self.soup.find('div', class_ = 'title ng-binding')\
                        .string.encode('utf-8').strip('\n')
        return self.encode2Character(title)

    #def get_num_followers(self):
