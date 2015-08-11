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

class Home(Entry):
    """ Tool class for getting homepage info """

    def __init__(self, session):
        Entry.__init__(self, session)

    def get_num_following_questions(self):
        """ Return number of following questions int. """
        rsp = self.session.get(Get_FQ_URL)
        soup = self.getSoup(rsp.content)
        num = soup.find('span', class_ = 'zg-gray-normal')\
                    .get_text(strip = True).encode(CODE)
        # num now is "(\d+)"
        num = re.search('\d+', num)
        return int(num.group(0))

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
        while not i % FQ_Item_Num:
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
        q = self.get_following_questions()
        eids = []
        try:
            while True:
                eids.append(q.next())
        except StopIteration: pass
        finally:
            return eids

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
        while not i % FC_Item_Num:
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
        c = self.get_following_collections()
        eids = []
        try:
            while True:
                eids.append(c.next())
        except StopIteration: pass
        finally:
            return eids
