# -*- coding: utf-8 -*-

from Entry import Entry
from Iterator import AIterator, TIterator

class Question(Entry):
    """ Tool class for getting question info """

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
                        .div.a.stong.string.encode('utf-8')
        return int(num)

    # generator for getting topics
    def get_topics(self):
        return TIterator(self)
        #topic = self.soup.find('a', class_ = 'zm-item-tag')
        #while topic:
        #    url = topic['href']
        #    yield url
        #    topic = topic.find_next_sibling('a', class_ = 'zm-item-tag')
        #print "No more topics"

    # generator for getting answers
    def get_answers(self):
        return AIterator(self)
        #answer = self.soup.find('div', class_ = 'zm-item-answer ')
        #while answer:
        #    url = "/question/{0}/answer/{1}".format(self.Eid, answer['data-atoken'])
        #    yield url
        #    answer = answer.find_next_sibling('div', class_ = 'zm-item-answer ')
        #print "No more answers."