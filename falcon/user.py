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

class User(Entry):
    """ Tool class for getting user info. """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_name(self):
        """ Return user name text. """
        name = self.soup.find('div', class_ = 'title-section ellipsis').find('span', class_ = 'name')\
                        .get_text(strip = True).encode(CODE)
        return name

    def get_biography(self):
        """ Return user biography text or None. """
        bio = self.soup.find('span', class_ = 'bio')
        if bio:
            return bio.get_text(strip = True).encode(CODE)
        return None

    def _get_about_item(self, name):
        """
        Return user about item dictionary
        { 'name' : {
            'text' : '...', 
            'topic' : topic-eid
            }
        }
        """
        item = {}
        text = self.soup.find('span', class_  = name + ' item')
        if text:
            item['text'] = text.get_text(strip = True).encode(CODE)
            topic = text.find('a')
            if topic:
                item['topic'] = topic['href']
        return item

    def get_about(self):
        """
        Return all user abouts in dictionary, including
        'location', 'business', 'employment', 'position', 'education', 'education-extra',
        """
        about = {}
        about['location'] = self._get_about_item('location')
        about['business'] = self._get_about_item('business')
        about['employment'] = self._get_about_item('employment')
        about['position'] = self._get_about_item('position')
        about['education'] = self._get_about_item('education')
        about['education-extra'] = self._get_about_item('education-extra')
        return about

    def get_description(self):
        """ Return user description text or None. """
        des = self.soup.find('div', attrs = {'data-name' : 'description'})
        if des:
            return des.find('span', class_ = 'content')\
                    .get_text(strip = True).encode(CODE)
        return None

    @return_int
    def get_num_followees(self):
        """ Return number of followees int. """
        return self.soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[0].strong\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_followers(self):
        """ Return number of followers int. """
        return self.soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong\
                        .get_text(strip = True).encode(CODE)
        
    @return_int
    def get_num_agrees(self):
        """ Return number of agrees int. """
        return self.soup.find('span', class_ = 'zm-profile-header-user-agree').strong\
                        .get_text(strip = True).encode(CODE)
        
    @return_int
    def get_num_thanks(self):
        """ Return number of thanks int. """
        return self.soup.find('span', class_ = 'zm-profile-header-user-thanks').strong\
                        .get_text(strip = True).encode(CODE)
        
    @return_int
    def get_num_asks(self):
        """ Return number of asks int. """
        return self.soup.find_all("span", class_ = "num")[0]\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_answers(self):
        """ Return number of answers int. """
        return self.soup.find_all("span", class_ = "num")[1]\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_posts(self):
        """ Return number of posts int. """
        return self.soup.find_all("span", class_ = "num")[2]\
                        .get_text(strip = True).encode(CODE)
        
    @return_int
    def get_num_collections(self):
        """ Return number of collections int. """
        return self.soup.find_all("span", class_ = "num")[3]\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_logs(self):
        """ Return number of logs int. """
        return self.soup.find_all("span", class_ = "num")[4]\
                        .get_text(strip = True).encode(CODE)

    def get_followees(self):
        """ A generator yields a followee eid per next().  """
        rsp = self.session.get(self.url + "/followees")
        soup = self.getSoup(rsp.content)
        followees = soup.find_all('div', class_ = 'zm-profile-card zm-profile-section-item zg-clear no-hovercard')
        if not followees:
            return
        i, followee = 0, None
        for followee in followees:
            i += 1
            yield followee.a['href']
        while not i % Page_Items_Num:
            data = {
                'method' : 'next',
                'params' : json.dumps({
                    'offset' : i,
                    'order_by' : "created",
                    'hash_id' : self.soup.find('button', attrs = {'data-follow' : 'm:button'})['data-id']
                    }),
                '_xsrf' : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(Get_More_Followees_URL, data = data)
            if rsp.json()['r'] == 0:
                followees = rsp.json()['msg']
                for followee in followees:
                    i += 1
                    yield self.getSoup(followee).a['href']
            else:
                return

    def get_all_followees(self):
        """ Return a [list] of followee eids. """
        return get_all_(self.get_followees)
    
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
            yield follower.a['href']
        while not i % Page_Items_Num:
            data = {
                'method' : 'next',
                'params' : json.dumps({
                    'offset' : i,
                    'order_by' : "created",
                    'hash_id' : self.soup.find('button', attrs = {'data-follow' : 'm:button'})['data-id']
                    }),
                '_xsrf' : self.session.getCookie()['_xsrf']
                }
            rsp = self.session.post(Get_More_Followers_URL, data = data)
            if rsp.json()['r'] == 0:
                followers = rsp.json()['msg']
                for follower in followers:
                    i += 1
                    yield self.getSoup(follower).a['href']
            else:
                return

    def get_all_followers(self):
        """ Return a [list] of follower eids. """
        return get_all_(self.get_followers)
        
    def get_asks(self):
        """ A generator yields a question eid per next().  """
        rsp = self.session.get(self.url + "/asks")
        soup = self.getSoup(rsp.content)
        questions = soup.find_all('div', class_ = 'zm-profile-section-item zg-clear')
        if not questions:
            return
        i, question = 2, None
        for question in questions:
            yield question.h2.a['href']
        while True:
            params = {'page' : i}
            i += 1
            rsp = self.session.get(self.url + "/asks", params = params)
            soup = self.getSoup(rsp.content)
            questions = soup.find_all('div', class_ = 'zm-profile-section-item zg-clear')
            if questions:
                for question in questions:
                    yield question.h2.a['href']
            else:
                return

    def get_all_asks(self):
        """ Return a [list] of question eids. """
        return get_all_(self.get_asks)

    def get_answers(self):
        """ A generator yields a answer eid per next().  """
        rsp = self.session.get(self.url + "/answers")
        soup = self.getSoup(rsp.content)
        answers = soup.find_all('div', class_ = 'zm-item')
        if not answers:
            return
        i, answer = 2, None
        for answer in answers:
            yield answer.h2.a['href']
        while True:
            params = {'page' : i}
            i += 1
            rsp = self.session.get(self.url + "/answers", params = params)
            soup = self.getSoup(rsp.content)
            answers = soup.find_all('div', class_ = 'zm-item')
            if answers:
                for answer in answers:
                    yield answer.h2.a['href']
            else:
                return

    def get_all_answers(self):
        """ Return a [list] of answer eids. """
        return get_all_(self.get_answers)

    def get_collections(self):
        """ A generator yields a collection eid per next().  """
        rsp = self.session.get(self.url + "/collections")
        soup = self.getSoup(rsp.content)
        collections = soup.find_all('div', class_ = 'zm-profile-section-item zg-clear')
        if not collections:
            return
        i, collection = 2, None
        for collection in collections:
            yield collection.a['href']
        while True:
            params = {'page' : i}
            i += 1
            rsp = self.session.get(self.url + "/collections", params = params)
            soup = self.getSoup(rsp.content)
            collections = soup.find_all('div', class_ = 'zm-profile-section-item zg-clear')
            if collections:
                for collection in collections:
                    yield collection.a['href']
            else:
                return

    def get_all_collections(self):
        """ Return a [list] of collection eids. """
        return get_all_(self.get_collections)

    def follow_me(self, action = 'follow'):
        """ Follow|Unfollow this user. Return status code. """
        data = {
            'params' : json.dumps({
                'hash_id' : self.soup.find('button', attrs = {'data-follow' : 'm:button'})['data-id']
                }),
            '_xsrf' : self.session.getCookie()['_xsrf']
            }
        data['method'] = 'follow_member' if action == 'follow' else\
                        'unfollow_member'
        rsp = self.session.post(Follow_User_URL, data)
        if rsp.status_code == requests.codes.ok:
            return SUCCESS
        else:
            return FAILURE

    def unfollow_me(self):
        """ Unfollow this user, Return status code. """
        return self.follow_me('unfollow')
