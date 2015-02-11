# -*- coding: utf-8 -*-

import requests
import json
from Entry import Entry

class Question(Entry):
    """ Tool class for getting question info """

    PageSize = 50
    FollowerSize = 20

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        title = self.soup.find('h2', class_ = 'zm-item-title')\
                        .string.encode('utf-8').strip('\n')
        return self.encode2Character(title)

    def get_description(self):
        description = self.soup.find('div', id = 'zh-question-detail')\
                                .div.get_text().encode('utf-8').strip('\n')
        return self.encode2Character(description)

    def get_num_answers(self):
        num = self.soup.find('h3', id = 'zh-question-answer-num')
        if num:
            return int(num['data-num'])
        return 0

    def get_num_followers(self):
        num = self.soup.find('div', class_ = 'zh-question-followers-sidebar')\
                        .div.a.strong.string.encode('utf-8')
        return int(num)

    # generator section start #

    def get_topics(self):
        topic = self.soup.find('a', class_ = 'zm-item-tag')
        while topic:
            url = topic['href']
            yield url
            topic = topic.find_next_sibling('a', class_ = 'zm-item-tag')
        print "No more topics"

    def get_related_questions(self):
        question = self.soup.find('ul', itemprop = 'relatedQuestion').li
        while question:
            url = question.a['href']
            yield url
            question = question.find_next_sibling('li')
        print "No more related questions"

    def _get_answer_list_v2(self, url, i):
        """
        Private API to use async post to get more answers.
        i is the couter of posts, used to evaluate the offset.
        Return a content list.
        """
        data = {
            'method' : 'next',
            'params' : json.dumps({
                'url_token' : self.get_id(),
                'pagesize' : Question.PageSize,
                'offset' : Question.PageSize * i
                }),
            '_xsrf' : self.session.getCookie()['_xsrf']
            }
        rsp = self.session.post(url, data)
        if rsp.status_code == requests.codes.ok:
            return rsp.json()["msg"]

    def get_answers(self):
        answer = None
        answer_list = []
        a_url = self.session._HOST_ + "/node/QuestionAnswerListV2"
        for i in xrange(self.get_num_answers()):
            if i == 0:
                answer = self.soup.find('div', class_ = 'zm-item-answer ')
            elif i < Question.PageSize:
                answer = answer.find_next_sibling('div', class_ = 'zm-item-answer ')
            else:
                if not i % Question.PageSize:
                    answer_list = self._get_answer_list_v2(a_url, i/Question.PageSize)
                answer = self.getSoup(answer_list[i % Question.PageSize]).find('div')
            url = "/question/{0}/answer/{1}".format(self.get_id(), answer['data-atoken'])
            yield url
        print "No more answers."


    def _get_follower_content(self, url, i):
        """
        Private API to use async post to get more followers.
        i is the couter of posts, used to evaluate the offset.
        Return new HTML content.
        """
        data = {
            'start' : 0,
            'offset' : Question.FollowerSize * i,
            '_xsrf' : self.session.getCookie()['_xsrf']
            }
        rsp = self.session.post(url, data)
        if rsp.status_code == requests.codes.ok:
            return rsp.json()["msg"][1]

    def get_followers(self):
        soup = None
        follower = None
        f_url = self.session._HOST_ + self.url + "/followers"

        rsp = self.session.get(f_url)
        if rsp.status_code == requests.codes.ok:
            soup = self.getSoup(rsp.content)

        for i in xrange(self.get_num_followers()):
            if i == 0:
                follower = soup.find('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
            elif i < Question.FollowerSize:
                follower = follower.find_next_sibling('div')
            else:
                if not i % Question.FollowerSize:
                    content = self._get_follower_content(f_url, i/Question.FollowerSize)
                    soup = self.getSoup(content)
                    follower = soup.find('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
                else:
                    follower = follower.find_next_sibling('div')
            url = follower.find('a', class_ = 'zm-item-link-avatar')['href']
            yield url
        print "No more followers"

    # get generator section end #