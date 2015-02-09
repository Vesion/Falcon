# -*- coding: utf-8 -*-

from Entry import Entry
from User import User

class Answer(Entry):
    """ Tool class for getting answer info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_author(self):
        author = self.soup.find('div', id = 'js-sidebar-author-info')\
                            .find('h2', class_ = 'zm-list-content-title').a
        if author:
            url = author['href'].split('/')[-1];
            return User(self.session, '/people/'+url)
        else:
            return None # anonymous user