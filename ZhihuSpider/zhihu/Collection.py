# -*- coding: utf-8 -*-

from Entry import Entry
from User import User

class Collection(Entry):
    """ Tool class for getting collection info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        name = self.soup.find('h2', id = 'zh-fav-head-title')\
                        .string.encode('utf-8').strip('\n')
        return self.decode2Character(name)

    def get_creator(self):
        url = self.soup.find('h2', class_ = 'zm-list-content-title')\
                        .a['href'].encode('utf-8').strip('\n')
        return User(self.session, url)