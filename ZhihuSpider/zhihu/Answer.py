# -*- coding: utf-8 -*-

from Entry import Entry
from User import User
import re

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

    def get_num_upvotes(self):
        num = self.soup.find('span', class_ = 'count').string
        if num[-1] == "K":
            return int(num[:-1]) * 1000
        elif num[-1] == "W":
            return int(num[:-1]) * 10000
        return int(num)

    def get_num_comments(self):
        num = self.soup.find('a', class_ = ' meta-item toggle-comment')\
                        .get_text().encode('utf-8').strip('\n')
        num = re.search('\d+', num)
        if num:
            return int(num.group(0))
        return 0
