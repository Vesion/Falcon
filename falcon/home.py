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

class Home(Entry):
    """ Tool class for getting homepage info. """

    def __init__(self, session):
        Entry.__init__(self, session)

    @return_int
    def get_num_following_questions(self):
        """ Return number of following questions int. """
        rsp = self.session.get(Get_FQ_URL)
        soup = self.getSoup(rsp.content)
        return soup.find('span', class_ = 'zg-gray-normal')\
                    .get_text(strip = True).encode(CODE)

    def get_following_questions(self):
        """ A generator yields a question eid per next().  """
        rsp = self.session.get(Get_FQ_URL)
        soup = self.getSoup(rsp.content)
        questions = soup.find_all('div', class_ = 'zm-profile-section-item zg-clear')
        if not questions:
            return
        i, question = 0, None
        for question in questions:
            i += 1
            yield question.find('a')['href']
        while not i % Page_Items_Num:
            data = {
                'method' : 'next',
                'params' : json.dumps({
                    'offset' : i
                    }),
                '_xsrf'  : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(Get_More_FQ_URL, data)
            if rsp.json()['r'] == 0:
                questions = self.getSoup(rso.json()['msg']).find_all('div', class_ = 'zm-profile-section-item zg-clear')
                for question in questions:
                    i += 1
                    yield question.find('a')['href']
            else:
                return

    def get_all_following_questions(self):
        """ Return a [list] of following questions eids. """
        return get_all_(self.get_following_questions)

    def get_following_collections(self):
        """ A generator yields a collection eid per nex(). """
        rsp = self.session.get(Get_FC_URL)
        soup = self.getSoup(rsp.content)
        collections = soup.find_all('div', class_ = 'zm-item')
        if not collections:
            return
        i, collection = 0, None
        for collection in collections:
            i += 1
            yield collection.h2.a['href']
        while not i % Page_Items_Num:
            data = {
                    'offset' : i,
                    'start'  : collection['id'].split('-')[-1],
                    '_xsrf'  : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(Get_More_FC_URL, data)
            if rsp.json()['r'] == 0:
                collections = self.getSoup(rsp.json()['msg'][1]).find_all('div', class_ = 'zm-item')
                for collection in collections:
                    i += 1
                    yield collection.h2.a['href']
            else:
                return

    def get_all_following_collections(self):
        """ Return a [list] of following collection eids. """
        return get_all_(self.get_following_collections)
