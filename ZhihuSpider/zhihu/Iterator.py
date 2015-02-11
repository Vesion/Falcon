class Iterator:
    """
    Base class for specified iterator tool classes.
    """
    def __init__(self, entry):
        self.entry = entry

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

class AIterator(Iterator):

    def __init__(self, entry):
        Iterator.__init__(self, entry)
        self.answer = self.entry.soup.find('div', class_ = 'zm-item-answer ')

    def next(self):
        if self.answer:
            url = "/question/{0}/answer/{1}".format(self.entry.get_id(), self.answer['data-atoken'])
            self.answer = self.answer.find_next_sibling('div', class_ = 'zm-item-answer ')
            return url
        else:
            raise StopIteration()

class TIterator(Iterator):

    def __init__(self, entry):
        Iterator.__init__(self, entry)
        self.topic = self.entry.soup.find('a', class_ = 'zm-item-tag')

    def next(self):
        if self.topic:
            url = self.topic['href']
            self.topic = self.topic.find_next_sibling('a', class_ = 'zm-item-tag')
            return url
        else:
            raise StopIteration()
