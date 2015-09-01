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

class Question(Entry):
    """ Tool class for getting question info. """

    AnswerSize = 50 # For answers page
    FollowerSize = 20 # For followers page

    def __init__(self, session, eid):
        Entry.__init__(self, session, eid)

    def get_title(self):
        """ Return question title string. """
        return self.soup.find('div', id = 'zh-question-title').h2\
                        .get_text(strip = True).encode(CODE)

    def get_description(self):
        """ Return question description string. """
        return self.soup.find('div', id = 'zh-question-detail').div\
                                .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_answers(self):
        """ Return number of answers int. """
        num = self.soup.find('h3', id = 'zh-question-answer-num')
        if num:
            return num.get_text(strip = True).encode(CODE)
        return ''

    @return_int
    def get_num_followers(self):
        """ Return number of followers int. """
        num = self.soup.find('div', class_ = 'zh-question-followers-sidebar').div.a
        if num:
            return num.strong.get_text(strip = True).encode(CODE)
        return ''
    
    def get_topics(self):
        """ Return a [list] of in-topic eids. """
        eids = []
        topics = self.soup.find_all('a', class_ = 'zm-item-tag')
        for topic in topics:
            eids.append(topic['href'])
        return eids
        
    def get_related_questions(self):
        """ Return a [list] of related question eids. """
        eids = []
        questions = self.soup.find_all('li', itemprop = 'itemListElement')
        for question in questions:
            eids.append(question.a['href'])
        return eids

    def get_followers(self):
        """ A generator yields a follower eid per next().  """
        rsp = self.session.get(self.url + "/followers")
        soup = self.getSoup(rsp.content)
        followers = soup.find_all('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
        if not followers:
            return
        i, follower = 0, None
        for follower in followers:
            i += 1
            if follower.find('a'): # for anonymous user
                yield follower.a['href']
        while not i % Page_Items_Num:
            data = {
                'offset' : i,
                'start'  : 0,
                '_xsrf'  : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(self.url + "/followers", data = data)
            if rsp.json()['r'] == 0:
                followers = self.getSoup(rsp.json()['msg'][1]).find_all('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
                for follower in followers:
                    i += 1
                    if follower.find('a'): # ditto
                        yield follower.a['href']
            else:
                return

    def get_all_followers(self):
        """ Return a [list] of follower eids. """
        return get_all_(self.get_followers)

    def get_answers(self):
        """ A generator yields a answer eid per next().  """
        answers = self.soup.find_all('div', class_ = 'zm-item-answer ')
        if not answers:
            return
        i, answer = 0, None
        for answer in answers:
            i += 1
            answer = answer.find('a', class_ = 'answer-date-link')
            if answer: # some answers are shielded
                yield answer['href']
        while not i % Page_Answers_Num:
            data = {
                'method' : 'next',
                'params' : json.dumps({
                    'url_token' : self.eid.split('/')[-1],
                    'pagesize' : Page_Answers_Num,
                    'offset' : i
                    }),
                '_xsrf' : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(Get_More_Answers_URL, data = data)
            if rsp.json()['r'] == 0:
                answers = rsp.json()['msg']
                for answer in answers:
                    i += 1
                    answer = self.getSoup(answer).find('a', class_ = 'answer-date-link')
                    if answer: # ditto
                        yield answer['href']
            else:
                return

    def get_all_answers(self):
        """ Return a [list] of answer eids. """
        return get_all_(self.get_answers)

    def get_all_collapsed_answers(self):
        """ Return a [list] of shielded answer eids. """
        eids = []
        if self.soup.find('div', attrs = {'id' : 'zh-question-collapsed-link', 'style' : 'display:'}):
            params = {
                'params' : json.dumps({
                    'question_id':self.soup.find('div', id = 'zh-question-detail')['data-resourceid']})
                }
            rsp = self.session.get(Get_Collapsed_Answers_URL, params = params)
            soup = self.getSoup(rsp.content)
            answers = soup.find_all('div', class_ = 'zm-item-answer ')
            for answer in answers:
                answer = answer.find('a', class_ = 'answer-date-link')
                if answer: # some answers are shielded
                    eids.append(answer['href'])
        return eids

    def follow_me(self, action = 'follow_question'):
        """ Follow this question. Return status code. """
        data = {
            'params' : json.dumps({
                'question_id' : self.soup.find('div', id = 'zh-question-detail')['data-resourceid']
                }),
            '_xsrf'  : self.session.getCookie()['_xsrf'],
            'method' : action
            }
        rsp = self.session.post(Follow_Question_URL, data)
        if rsp.status_code == requests.codes.ok:
            return SUCCESS
        else:
            return FAILURE

    def unfollow_me(self):
        """ Unfollow this collection. Return status code. """
        return self.follow_me('unfollow_question')
