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

class Topic(Entry):
    """ Tool class for getting topic info. """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_name(self):
        """ Return topic name string. """
        return self.soup.find('div', id = 'zh-topic-title').h1\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_followers(self):
        """ Return number of followers int. """
        a = self.soup.find('div', class_ = 'zm-topic-side-followers-info').a
        if a:
            return a.get_text(strip = True).encode('utf-8')
        return ''

    def get_description(self):
        """ Return description string or None. """
        des = self.soup.find('div', id = 'zh-topic-desc').find('div', class_ = 'zm-editable-content')
        if des:
            return des.get_text(strip = True).encode(CODE)
        return None

    def get_followers(self):
        """ A generator yields a follower eid per next().  """
        rsp = self.session.get(self.url + "/followers")
        soup = self.getSoup(rsp.content)
        followers = soup.find_all('div', class_ = 'zm-person-item')
        if not followers:
            return
        i, follower = 0, None
        for follower in followers:
            i += 1
            yield follower.find('a', recursive = False)['href']
        while not i % Page_Items_Num:
            data = {
                    'offset' : i,
                    'start'  : follower['id'].split('-')[-1],
                    '_xsrf'  : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(self.url + "/followers", data = data)
            if rsp.json()['r'] == 0:
                followers = self.getSoup(rsp.json()['msg'][1]).find_all('div', class_ = 'zm-person-item')
                for follower in followers:
                    i += 1
                    yield follower.find('a', recursive = False)['href']
            else:
                return

    def get_all_followers(self):
        """ Return a [list] of follower eids. """
        return get_all_(self.get_followers)

    def follow_me(self, action = 'follow'):
        """ Follow this topic. Return status code. """
        data = {
            'params' : json.dumps({
                'topic_id' : self.soup.find('div', id = 'zh-topic-desc')['data-resourceid']
                }),
            '_xsrf' : self.session.getCookie()['_xsrf']
            }
        data['method'] = 'follow_topic' if action == 'follow' else\
                        'unfollow_topic'
        rsp = self.session.post(Follow_Topic_URL, data)
        if rsp.status_code == requests.codes.ok:
            return SUCCESS
        else:
            return FAILURE

    def unfollow_me(self):
        """ Unfollow this topic, Return status code. """
        return self.follow_me('unfollow')

    # TODO #

    def get_hot(self):
        """ """

    def get_newest(self):
        """ """

    def get_top_answers(self):
        """ """

    def get_questions(self):
        """ """

