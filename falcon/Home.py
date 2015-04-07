# -*- coding: utf-8 -*-

import sys
import requests
import json
import re

from Entry import Entry

class Home(Entry):
    """ Tool class for getting home personal info """

    def __init__(self, session):
        Entry.__init__(self, session)


    def get_all_following_questions(self, limit = sys.maxsize):
        """ Return limit/all following questions url list. """

        PageSize = 20
        fg_url = self.session._HOST_ + "/question/following"
        fp_url = self.session._HOST_ + "/node/ProfileFollowedQuestionsV2"

        question = None
        question_list = []
        soup = None

        rsp = self.session.get(fg_url)
        if rsp.status_code == requests.codes.ok:
            soup = self.getSoup(rsp.content)

        def get_num_following_questions():
            num = soup.find('span', class_ = 'zg-gray-normal')\
                        .get_text(strip = True).encode('utf-8')
            num = re.search('\d+', num)
            if num:
                return int(num.group(0))
            return 0

        def get_following_questions():
            """
            First get the following question page.
            The original page has `PageSize` questions at most for search.
            Then use AJAX post to get `PageSize` questions each time until reach max.
            """

            for i in xrange(get_num_following_questions()):
                if i == 0:
                    question = soup.find('div', class_ = 'zm-profile-section-item zg-clear')
                elif i < PageSize:
                    question = question.find_next_sibling('div')
                else:
                    if not i % PageSize:
                        data = {
                            'method' : 'next',
                            'params' : json.dumps({
                                'offset' : PageSize * (i/PageSize)
                                }),
                            '_xsrf' : self.session.getCookie()['_xsrf']
                            }
                        rsp = self.session.post(fp_url, data)
                        if rsp.status_code == requests.codes.ok:
                            question_list = rsp.json()["msg"]
                    question = self.getSoup(question_list[i % PageSize]).find('div')
                url = question.find('a')['href']
                yield url
            print "No more followees."

        q = get_following_questions()
        return [q.next() for i in xrange(min(limit, get_num_following_questions()))]