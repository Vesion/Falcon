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
        """ A generator that yield a question url per next().  """
        rsp = self.session.get(Get_FQ_URL)
        soup = self.getSoup(rsp.content)

        fq_num = self.get_num_following_questions()
        question = None
        question_list = []

        for i in xrange(fq_num):
            if i == 0:
                question = soup.find('div', class_ = 'zm-profile-section-item zg-clear')
            elif i < FQ_Item_Num:
                question = question.find_next_sibling('div')
            else:
                if not i % FQ_Item_Num:
                    data = {
                        'method' : 'next',
                        'params' : json.dumps({
                            'offset' : FQ_Item_Num * (i/FQ_Item_Num)
                            }),
                        '_xsrf' : self.session.getCookie()['_xsrf']
                        }
                    rsp = self.session.post(Get_More_FQ_URL, data)
                    question_list = rsp.json()["msg"]
                question = self.getSoup(question_list[i % FQ_Item_Num]).find('div')
            url = question.find('a')['href']
            yield url
        print "No more followees."

    def get_all_following_questions(self):
        """ Return: A [list] of following questions urls. """
        q = self.get_following_questions()
        urls = []
        try:
            while True:
                urls.append(q.next())
        except StopIteration: pass
        finally:
            return urls
