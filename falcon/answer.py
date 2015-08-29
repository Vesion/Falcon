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
from .entry import Entry

class Answer(Entry):
    """ Tool class for getting answer info. """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_author(self):
        """ Return author eid or None. """
        author = self.soup.find('a', class_ = 'zm-item-link-avatar')
        if author:
            return author['href']
        return None # for anonymous user

    @return_int
    def get_num_upvotes(self):
        """ Return number of upvotes int.  """
        num = self.soup.find('div', class_ = 'answer-head').find_all('div')[1]['data-votecount']
        return num

    @return_int
    def get_num_comments(self):
        """ Return number of comments int. """
        return self.soup.find('a', class_ = ' meta-item toggle-comment')\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_collects(self):
        """ Return number of being collected int. """
        num = self.soup.find('a', href = self.eid + '/collections');
        if num:
            return num.get_text(strip = True).encode(CODE)
        return '0'

    def get_voters(self):
        """ A generator yields a voted user eid per next().  """
        aid = self.soup.find('div', class_='zm-item-answer')['data-aid']
        url = HOST_URL + "/answer/{0}/voters_profile".format(aid)
        while url:
            rsp = self.session.get(url) 
            voters = rsp.json()['payload']
            for voter in voters:
                voter = self.getSoup(voter).a
                if voter: # for anonymous user
                    yield voter['href']
            url = HOST_URL + rsp.json()['paging']['next']

    def get_all_voters(self):
        """ Return a [list] of voted user eids. """
        return get_all_(self.get_voters)

    def get_text_content(self):
        """ Return content text (no image link). """
        text = self.soup.find('div', class_ = ' zm-editable-content clearfix')\
                        .get_text(strip = 'utf-8').encode('utf-8')
        return self.encode2Character(text)

    # TODO #

    def get_comments(sefl):
        """ """
