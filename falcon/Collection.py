# -*- coding: utf-8 -*-

from Entry import Entry

class Collection(Entry):
    """ Tool class for getting collection info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        title = self.soup.find('h2', id = 'zh-fav-head-title')\
                        .string.encode('utf-8').strip('\n')
        return self.encode2Character(title)

    def get_creator(self):
        return self.soup.find('h2', class_ = 'zm-list-content-title')\
                        .a['href']
