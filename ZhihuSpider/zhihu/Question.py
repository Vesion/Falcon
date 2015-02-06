# -*- coding: utf-8 -*-

from Entry import Entry

class Question(Entry):
    """ Tool class for getting questions """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_title(self):
        title = self.soup.find("h2", class_ = "zm-item-title")\
                    .string.encode("utf-8")\
                    .replace("\n", "")
        return self.decode2Chinese(title)