# -*- coding: utf-8 -*-

from Entry import Entry
from Answer import Answer

class Question(Entry):
    """ Tool class for getting question info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

        self.next_answer = self.__next_answer()

    def get_title(self):
        title = self.soup.find('h2', class_ = 'zm-item-title')\
                        .string.encode('utf-8').strip('\n')
        return self.decode2Character(title)

    def get_description(self):
        description = self.soup.find('div', id = 'zh-question-detail')\
                                .div.get_text()\
                                .encode('utf-8')
        return self.decode2Character(description)

    def get_in_topics(self):
        topics = self.soup.find_all('a', class_ = 'zm-item-tag')
        return map(lambda x : self.decode2Character(x), 
                   [i.contents[0].encode("utf-8").strip('\n') for i in topics])

    def get_num_answers(self):
        num = self.soup.find('h3', id = 'zh-question-answer-num')
        if num:
            return int(num['data-num'])
        return 0

    def get_num_followers(self):
        num = self.soup.find('div', class_ = 'zg-gray-normal')\
                        .a.stong.string
        return int(num)

    # public iterator API for getting answer
    def get_next_answer(self):
        return self.next_answer.next()

    # private generator for getting answer
    def __next_answer(self):
        answer = self.soup.find('div', class_ = 'zm-item-answer ')
        while answer:
            answer_url = "/question/{0}/answer/{1}".format(self.Eid, answer['data-atoken'])
            yield Answer(self.session, answer_url)
            answer = answer.find_next_sibling()
        print "No more answers."