# -*- coding: utf-8 -*-

import re

from Entry import Entry

class Answer(Entry):
    """ Tool class for getting answer info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    # Note: This API may return empty string due to anonymous user
    def get_author(self):
        author = self.soup.find('div', id = 'js-sidebar-author-info')\
                            .find('h2', class_ = 'zm-list-content-title').a
        if author:
            return author['href']
        return None # anonymous user

    def get_num_upvotes(self):
        num = self.soup.find('span', class_ = 'count').string.encode('utf-8')
        if num[-1] == "K":
            return int(num[:-1]) * 1000
        elif num[-1] == "W":
            return int(num[:-1]) * 10000
        return int(num)

    def get_num_comments(self):
        num = self.soup.find('a', class_ = ' meta-item toggle-comment')\
                        .get_text().encode('utf-8')
        num = re.search('\d+', num)
        if num:
            return int(num.group(0))
        return 0

    def get_text_content_text(self):
        text = self.soup.find('div', class_ = ' zm-editable-content clearfix')\
                        .get_text().encode('utf-8').strip('\n')
        return self.encode2Character(text)
