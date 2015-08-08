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

class Collection(Entry):
    """ Tool class for getting collection info. """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        """ Return title text. """
        return self.soup.find('h2', id = 'zh-fav-head-title')\
                        .get_text(strip = True).encode(CODE)

    def get_creator(self):
        """ Return creator url. """
        return self.soup.find('h2', class_ = 'zm-list-content-title')\
                        .a['href']

    def get_items(self, itype):
        """ A generator that yield a question|answer url per next(). """

        def get_page_items(soup):
            items = soup.find_all('div', class_='zm-item')
            if len(items) == 0:
                yield None
                return
            else:
                for item in items:
                    if itype == 'question':
                        if item.h2:
                            yield item.h2.a['href']
                    elif itype == 'answer':
                        yield item.find('a', class_ = 'answer-date-link')['href']

        for url in get_page_items(self.soup):
            yield url
        i = 2
        while True:
            params = {'page' : i}
            rsp = self.session.get(self.url, params = params)
            soup = self.getSoup(rsp.content)
            for url in get_page_items(soup):
                if not url:
                    return
                yield url
            i += 1

    def get_all_items(self, itype):
        """ Return: A [list] of question|answer urls. """
        q = self.get_questions() if itype == 'question' else\
            self.get_answers()
        urls = []
        try:
            while True:
                urls.append(q.next())
        except StopIteration: pass
        finally:
            return urls

    def get_questions(self):
        """ Call get_items with question. """
        return self.get_items('question')

    def get_all_questions(self):
        """ Call get_all_items with question. """
        return self.get_all_items('question')

    def get_answers(self):
        """ Call get_items with answer. """
        return self.get_items('answer')

    def get_all_answers(self):
        """ Call get_all_items with answer. """
        return self.get_all_items('answer')

    def follow_it(self):
        """ Follow this collection. Return status code. """
        favlist_id = self.soup.find('div', id = 'zh-list-side-head')\
                                .a['id'].split('-')[-1]
        data = {
            'favlist_id' : favlist_id,
            '_xsrf'      : self.session.getCookie()['_xsrf']
            }
        rsp = self.session.post(Follow_Collection_URL, data)
        if rsp.status_code == requests.codes.ok:
            print "Follow this collection successfully!"
            return SUCCESS
        else:
            print "Fail to follow this collection"
            return FAILURE
