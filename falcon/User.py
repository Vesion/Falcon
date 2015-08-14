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

class User(Entry):
    """ Tool class for getting user info. """

    PageSize = 20

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

    # generator section start #

    def get_answers(self):
        """
        First get the answer page.
        Each page has `PageSize` answers at most.
        Get next page each time until reach max.
        """
        soup = None
        ansewr = None
        a_url = self.session._HOST_ + self.url + "/answers"
        params = {'page' : 1}

        for i in xrange(self.get_num_answers()):
            if not i % User.PageSize:
                rsp = self.session.get(a_url, params = params)
                params['page'] += 1
                soup = self.getSoup(rsp.content)
                answer = soup.find('div', id = 'zh-profile-answer-list').div
            else:
                answer = answer.find_next_sibling('div')
            url = answer.h2.a['href']
            yield url
        print "No more answers"

    def get_asks(self):
        """
        First get the ask page.
        Each page has `PageSize` asks at most.
        Get next page each time until reach max.
        """
        soup = None
        ask = None
        a_url = self.session._HOST_ + self.url + "/asks"
        params = {'page' : 1}

        for i in xrange(self.get_num_asks()):
            if not i % User.PageSize:
                rsp = self.session.get(a_url, params = params)
                params['page'] += 1
                soup = self.getSoup(rsp.content)
                ask = soup.find('div', id = 'zh-profile-ask-list').div
            else:
                ask = ask.find_next_sibling('div')
            url = ask.find('a', class_ = 'question_link')['href']
            yield url
        print "No more asks"

    def get_followees(self):
        """
        First get the followee page.
        The original page has `PageSize` followees at most for search.
        Then use AJAX post to get `PageSize` followees each time until reach max.
        """
        followee = None
        followee_list = []
        soup = None
        fg_url = self.session._HOST_ + self.url + "/followees"
        fp_url = self.session._HOST_ + "/node/ProfileFolloweesListV2"

        rsp = self.session.get(fg_url)
        soup = self.getSoup(rsp.content)
        
        for i in xrange(self.get_num_followees()):
            if i == 0:
                followee = soup.find('div', class_ = 'zh-general-list clearfix').div
            elif i < User.PageSize:
                followee = followee.find_next_sibling('div')
            else:
                if not i % User.PageSize:
                    data = {
                        'method' : 'next',
                        'params' : json.dumps({
                            'offset' : User.PageSize * (i/User.PageSize),
                            'order_by' : "created",
                            'hash_id' : self.soup.find('button', attrs = {'data-follow' : 'm:button'})['data-id']
                            }),
                        '_xsrf' : self.session.getCookie()['_xsrf']
                        }
                    rsp = self.session.post(fp_url, data)
                    followee_list = rsp.json()["msg"]
                followee = self.getSoup(followee_list[i % User.PageSize]).find('div')
            url = followee.find('a')['href']
            yield url
        print "No more followees."

    def get_followers(self):
        """
        First get the follower page.
        The original page has `FollowerSize` followers at most for search.
        Then use AJAX post to get `FollowerSize` followers each time until reach max.
        """
        follower = None
        follower_list = []
        soup = None
        fg_url = self.session._HOST_ + self.url + "/followers"
        fp_url = self.session._HOST_ + "/node/ProfileFollowersListV2"

        rsp = self.session.get(fg_url)
        soup = self.getSoup(rsp.content)
        
        for i in xrange(self.get_num_followers()):
            if i == 0:
                follower = soup.find('div', class_ = 'zh-general-list clearfix').div
            elif i < User.PageSize:
                follower = follower.find_next_sibling('div')
            else:
                if not i % User.PageSize:
                    data = {
                        'method' : 'next',
                        'params' : json.dumps({
                            'offset' : User.PageSize * (i/User.PageSize),
                            'order_by' : "created",
                            'hash_id' : self.soup.find('button', attrs = {'data-follow' : 'm:button'})['data-id']
                            }),
                        '_xsrf' : self.session.getCookie()['_xsrf']
                        }
                    rsp = self.session.post(fp_url, data)
                    follower_list = rsp.json()["msg"]
                follower = self.getSoup(follower_list[i % User.PageSize]).find('div')
            url = follower.find('a')['href']
            yield url
        print "No more followers."

    # generator section end #

    def get_all_answers(self, limit = sys.maxsize):
        """ Return limit/all answers url list. """
        ans = self.get_answers()
        return [ans.next() for i in xrange(min(limit, self.get_num_answers()))]

    def get_all_asks(self, limit = sys.maxsize):
        """ Return limit/all asks url list. """
        asks = self.get_asks()
        return [asks.next() for i in xrange(min(limit, self.get_num_asks()))]

    def get_all_followees(self, limit = sys.maxsize):
        """ Return limit/all followees url list. """
        fles = self.get_followees()
        return [fles.next() for i in xrange(min(limit, self.get_num_followees()))]
    
    def get_all_followers(self, limit = sys.maxsize):
        """ Return limit/all followers url list. """
        flrs = self.get_followers()
        return [flrs.next() for i in xrange(min(limit, self.get_num_followers()))]
        
