# -*- coding: utf-8 -*-

from Entry import Entry

class User(Entry):
    """ Tool class for getting people info """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_name(self):
        name = self.soup.find('div', class_ = 'title-section ellipsis')\
                            .find('span', class_ = 'name')\
                            .string.encode('utf-8')
        return self.decode2Character(name)

    def get_num_followees(self):
        num = self.soup.find('div', class_ = 'zm-profile-side-following zg-clear')\
                        .find_all('a')[0].strong.string
        return int(num)

    def get_num_followers(self):
        num = self.soup.find('div', class_ = 'zm-profile-side-following zg-clear')\
                        .find_all('a')[1].strong.string
        return int(num)

    def get_num_agrees(self):
        num = self.soup.find('span', class_ = 'zm-profile-header-user-agree')\
                        .strong.string
        return int(num)

    def get_num_thanks(self):
        num = self.soup.find('span', class_ = 'zm-profile-header-user-thanks')\
                        .strong.string
        return int(num)

    def get_num_asks(self):
        num = self.soup.find_all("span", class_ = "num")[0].string
        return int(num)

    def get_num_answers(self):
        num = self.soup.find_all("span", class_ = "num")[1].string
        return int(num)