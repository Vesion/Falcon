#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

from .Utils import *
from .Entry import Entry

class Collection(Entry):
    """ Tool class for getting collection info. """

    def __init__(self, session, eid):
        Entry.__init__(self, session, eid)

    def get_title(self):
        """ Return title text. """
        return self.soup.find('h2', id = 'zh-fav-head-title')\
                        .get_text(strip = True).encode(CODE)

    def get_creator(self):
        """ Return creator eid. """
        return self.soup.find('h2', class_ = 'zm-list-content-title')\
                        .a['href']

    def _get_items(self, itype):
        """ A generator yields a question|answer eid per next(). """

        def get_page_items(soup):
            items = soup.find_all('div', class_='zm-item')
            if not items:
                yield None # MUST yield None here.
                return
            for item in items:
                if itype == 'question':
                    if item.h2:
                        yield item.h2.a['href']
                elif itype == 'answer':
                    yield item.find('a', class_ = 'answer-date-link')['href']

        for eid in get_page_items(self.soup):
            yield eid
        i = 2
        while True:
            params = {'page' : i}
            rsp = self.session.get(self.url, params = params)
            soup = self.getSoup(rsp.content)
            for eid in get_page_items(soup):
                if not eid: # Due to yield None above, it works.
                    return
                yield eid
            i += 1

    def _get_all_items(self, itype):
        """ Return a [list] of question|answer eids. """
        i = self._get_items('question') if itype == 'question' else\
            self._get_items('answer')
        eids = []
        try:
            while True:
                eids.append(i.next())
        except StopIteration: pass
        finally:
            return eids

    def get_questions(self):
        """ Return generator with question. """
        return self._get_items('question')

    def get_answers(self):
        """ Return generator with answer. """
        return self._get_items('answer')

    def get_all_questions(self):
        """ Return a [list] of question eids. """
        return self._get_all_items('question')

    def get_all_answers(self):
        """ Return a [list] of answer eids. """
        return self._get_all_items('answer')

    def get_num_followers(self):
        """ Return number of followers int. """
        num = self.soup.find('a', href = self.eid + "/followers")\
                        .get_text(strip = True).encode(CODE)
        return int(num)

    def get_followers(self):
        """ A generator yields a user eid per next(). """
        rsp = self.session.get(self.url + "/followers")
        soup = self.getSoup(rsp.content)
        followers = soup.find_all('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
        if not followers:
            return
        i, follower = 0, None
        for follower in followers:
            i += 1
            yield follower.a['href']
        while not i % Page_Items_Num:
            data = {
                    'offset' : i,
                    '_xsrf'  : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(self.url + "/followers", data = data)
            if rsp.json()['r'] == 0:
                followers = self.getSoup(rsp.json()['msg'][1])\
                        .find_all('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
                for follower in followers:
                    i += 1
                    yield follower.a['href']
            else:
                return

    def get_all_followers(self):
        """ Return a [list] of user eids. """
        f = self.get_followers()
        eids = []
        try:
            while True:
                eids.append(f.next())
        except StopIteration: pass
        finally:
            return eids

    def follow_it(self):
        """ Follow this collection. Return status code. """
        favlist_id = self.soup.find('div', id = 'zh-list-side-head')\
                                .a['id'].split('-')[-1]
        data = {
            'favlist_id' : favlist_id,
            '_xsrf'      : self.session.getCookie()['_xsrf']
            }
        rsp = self.session.post(Follow_Collection_URL, data)
        if rsp.status_code == requests.codes.ok:
            print "Follow this collection successfully!"
            return SUCCESS
        else:
            print "Fail to follow this collection"
            return FAILURE
