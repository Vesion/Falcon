# -*- coding: utf-8 -*-

import sys
import requests
import json

from Entry import Entry

class Question(Entry):
    """ Tool class for getting question info """

    AnswerSize = 50 # For answers page
    FollowerSize = 20 # For followers page

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        """ Return question title text. """
        title = self.soup.find('h2', class_ = 'zm-item-title')\
                        .string.encode('utf-8').strip('\n')
        return self.encode2Character(title)

    def get_description(self):
        """ Return question description text. """
        description = self.soup.find('div', id = 'zh-question-detail')\
                                .div.get_text().encode('utf-8').strip('\n')
        return self.encode2Character(description)

    def get_num_answers(self):
        """ Return number of answers int or 0."""
        num = self.soup.find('h3', id = 'zh-question-answer-num')
        if num:
            return int(num['data-num'])
        return 0

    def get_num_followers(self):
        """ Return number of followers int."""
        num = self.soup.find('div', class_ = 'zh-question-followers-sidebar')\
                        .div.a.strong.string.encode('utf-8')
        return int(num)
    
    def get_topics(self):
        """ Return in topics url list."""
        urls = []
        topic = self.soup.find('a', class_ = 'zm-item-tag')
        while topic:
            url = topic['href']
            urls.append(url)
            topic = topic.find_next_sibling('a', class_ = 'zm-item-tag')
        return urls
        
    def get_related_questions(self):
        """ Return related questions url list."""
        urls = []
        question = self.soup.find('ul', itemprop = 'relatedQuestion').li
        while question:
            url = question.a['href']
            urls.append(url)
            question = question.find_next_sibling('li')
        return urls

    # generator section start #

    def get_answers(self):
        """
        The original page has `AnswerSize` answers at most for search.
        Then use AJAX post to get `AnswerSize` answers each time until reach max.
        """
        answer = None
        answer_list = []
        a_url = self.session._HOST_ + "/node/QuestionAnswerListV2"

        for i in xrange(self.get_num_answers()):
            if i == 0:
                answer = self.soup.find('div', class_ = 'zm-item-answer ')
            elif i < Question.AnswerSize:
                answer = answer.find_next_sibling('div', class_ = 'zm-item-answer ')
            else:
                if not i % Question.AnswerSize:
                    data = {
                        'method' : 'next',
                        'params' : json.dumps({
                            'url_token' : self.get_id(),
                            'pagesize' : Question.AnswerSize,
                            'offset' : Question.AnswerSize * (i / Question.AnswerSize)
                            }),
                        '_xsrf' : self.session.getCookie()['_xsrf']
                        }
                    rsp = self.session.post(a_url, data)
                    if rsp.status_code == requests.codes.ok:
                        answer_list = rsp.json()["msg"]
                answer = self.getSoup(answer_list[i % Question.AnswerSize]).find('div')
            url = "/question/{0}/answer/{1}".format(self.getId(), answer['data-atoken'])
            yield url
        print "No more answers."

    def get_followers(self):
        """
        First get the follower page.
        The original page has `FollowerSize` followers at most for search.
        Then use AJAX post to get `FollowerSize` followers each time until reach max.
        """
        follower = None
        soup = None
        f_url = self.session._HOST_ + self.url + "/followers"

        rsp = self.session.get(f_url)
        if rsp.status_code == requests.codes.ok:
            soup = self.getSoup(rsp.content)

        for i in xrange(self.get_num_followers()):
            if i == 0:
                follower = soup.find('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
            else:
                if not i % Question.FollowerSize:
                    data = {
                        'start' : 0,
                        'offset' : Question.FollowerSize * (i / Question.FollowerSize),
                        '_xsrf' : self.session.getCookie()['_xsrf']
                        }
                    rsp = self.session.post(f_url, data)
                    if rsp.status_code == requests.codes.ok:
                        soup = self.getSoup(rsp.json()["msg"][1])
                        follower = soup.find('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
                else:
                    follower = follower.find_next_sibling('div')
            link = follower.find('a', class_ = 'zm-item-link-avatar')
            if link:
                url = link['href']
                yield url
            else:
                yield None # anonymous user
        print "No more followers"

    # generator section end #

    def get_all_answers(self, limit = sys.maxsize):
        """ Return limit/all answers url list"""
        ans = self.get_answers()
        return [ans.next() for i in xrange(min(limit, self.get_num_answers()))]

    def get_all_followers(self, limit = sys.maxsize):
        """ Return limit/all followers url list"""
        fs = self.get_followers()
        return [fs.next() for i in xrange(min(limit, self.get_num_followers()))]
        