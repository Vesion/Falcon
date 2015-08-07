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


    def get_all_following_questions(self, num = sys.maxsize):
        """
        Get a [list] of my following questions urls.
        Params:
            num - The size of url list. If not provided, return all following urls.
        Return:
            A [list] of following questions urls.
        """

        question = None
        question_list = []
        soup = None

        rsp = self.session.get(Get_FQ_URL)
        soup = self.getSoup(rsp.content)

        def get_num_following_questions():
            num = soup.find('span', class_ = 'zg-gray-normal')\
                        .get_text(strip = True).encode(CODE)
            # num now is "(\d+)"
            num = re.search('\d+', num)
            return int(num.group(0))

        fq_num = get_num_following_questions()

        def get_following_questions():
            """
            First get the following question page.
            The original page has `FQ_Item_Num` questions at most for search.
            Then use AJAX post to get `FQ_Item_Num` questions each time until reach max.
            """

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

        q = get_following_questions()
        return [q.next() for i in xrange(min(num, fq_num))]
