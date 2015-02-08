# -*- coding: utf-8 -*-

from Entry import Entry

class Question(Entry):
    """ Tool class for getting question info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        title = self.soup.find('h2', class_ = 'zm-item-title')\
                        .string.encode('utf-8').strip('\n')
        return self.decode2Character(title)

    def get_description(self):
        description = self.soup.find('div', id = 'zh-question-detail')\
                                .div.get_text()\
                                .encode('utf-8')
        return self.decode2Character(description)

    def get_num_answers(self):
        num = self.soup.find('h3', id = 'zh-question-answer-num')
        if num:
            return int(num['data-num'])
        return 0

    def get_num_followers(self):
        num = self.soup.find('div', class_ = 'zg-gray-normal')\
                        .a.stong.string
        return int(num)

    def get_in_topics(self):
        topics = self.soup.find_all('a', class_ = 'zm-item-tag')
        return map(lambda x : self.decode2Character(x), 
                   [i.contents[0].encode("utf-8").strip('\n') for i in topics])

    #def get_all_answers(self):