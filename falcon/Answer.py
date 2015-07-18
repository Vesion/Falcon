#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

import re

from Entry import Entry

class Answer(Entry):
    """ Tool class for getting answer info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    # Note: This API may return empty string due to anonymous user
    def get_author(self):
        """ Return author url or None. """
        author = self.soup.find('div', id = 'js-sidebar-author-info')\
                            .find('h2', class_ = 'zm-list-content-title').a
        if author:
            return author['href']
        return None # anonymous user

    def get_num_upvotes(self):
        """ Return number of upvotes int.  """
        num = self.soup.find('span', class_ = 'count').get_text(strip = True).encode('utf-8')
        if num[-1] == "K":
            return int(num[:-1]) * 1000
        elif num[-1] == "W":
            return int(num[:-1]) * 10000
        return int(num)

    def get_num_comments(self):
        """ Return number of comments int or 0. """
        num = self.soup.find('a', class_ = ' meta-item toggle-comment')\
                        .get_text(strip = True).encode('utf-8')
        num = re.search('\d+', num)
        if num:
            return int(num.group(0))
        return 0

    def get_num_collects(self):
        """ Return number of being collected int or 0. """
        num = self.soup.find('a', href = self.url + '/collections');
        if num:
            return num.get_text(strip = True).encode('utf-8')
        return 0

    def get_text_content(self):
        """ Return content text (no image link). """
        text = self.soup.find('div', class_ = ' zm-editable-content clearfix')\
                        .get_text(strip = 'utf-8').encode('utf-8')
        return self.encode2Character(text)
