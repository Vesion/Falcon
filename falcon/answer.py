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

class Answer(Entry):
    """ Tool class for getting answer info. """

    def __init__(self, session, url):
        Entry.__init__(self, session, url)

    def get_author(self):
        """ Return author eid or None. """
        author = self.soup.find('a', class_ = 'zm-item-link-avatar')
        if author:
            return author['href']
        return None # for anonymous user

    def get_question(self):
        """ Return the eid of question where this answer in. """
        l = self.eid.split('/')
        return '/{0}/{1}'.format(l[1], l[2])

    @return_int
    def get_num_upvotes(self):
        """ Return number of upvotes int.  """
        num = self.soup.find('div', class_ = 'answer-head').find_all('div')[1]['data-votecount']
        return num

    @return_int
    def get_num_comments(self):
        """ Return number of comments int. """
        return self.soup.find('a', class_ = ' meta-item toggle-comment')\
                        .get_text(strip = True).encode(CODE)

    @return_int
    def get_num_collects(self):
        """ Return number of being collected int. """
        num = self.soup.find('a', href = self.eid + '/collections');
        if num:
            return num.get_text(strip = True).encode(CODE)
        return ''

    def get_voters(self):
        """ A generator yields a voted user eid per next().  """
        aid = self.soup.find('div', class_='zm-item-answer')['data-aid']
        url = HOST_URL + "/answer/{0}/voters_profile".format(aid)
        while url:
            rsp = self.session.get(url) 
            voters = rsp.json()['payload']
            for voter in voters:
                voter = self.getSoup(voter).a
                if voter: # for anonymous user
                    yield voter['href']
            url = HOST_URL + rsp.json()['paging']['next']

    def get_all_voters(self):
        """ Return a [list] of voted user eids. """
        return get_all_(self.get_voters)

    def vote_neutral(self, action = 'vote_neutral'):
        """ Vote neutral this answer. Return status code. """
        data = {
            'params' : json.dumps({
                'answer_id' : self.soup.find('div', class_='zm-item-answer')['data-aid']
                }),
            '_xsrf'  : self.session.getCookie()['_xsrf'],
            'method' : action
            }
        rsp = self.session.post(Vote_Neutral_Answer_URL, data)
        if rsp.status_code == requests.codes.ok:
            return SUCCESS
        else:
            return FAILURE

    def vote_up(self):
        """ Vote up this answer. Return status code. """
        return self.vote_neutral('vote_up')

    def vote_down(self):
        """ Vote down this answer. Return status code. """
        return self.vote_neutral('vote_down')

    def thanks(self, url = Thanks_Answer_URL):
        """ Thanks this answer. Return status code. """
        data = {
            'aid' : self.soup.find('div', class_='zm-item-answer')['data-aid'],
            '_xsrf'  : self.session.getCookie()['_xsrf'],
            }
        rsp = self.session.post(url, data)
        if rsp.status_code == requests.codes.ok:
            return SUCCESS
        else:
            return FAILURE

    def cancel_thanks(self):
        """ Cancel thanks this answer. Return status code. """
        return self.thanks(Cancel_Thanks_Answer_URL)

    def helpful(self, url = Helpful_Answer_URL):
        """ This answer is helpful to me. Return status code. """
        return self.thanks(Helpful_Answer_URL)

    def not_helpful(self):
        """ This answer is not helpful to me. Return status code. """
        return self.thanks(Not_Helpful_Answer_URL)

    def get_content(self):
        """ Return answer content in pretty soup format. """
        content = self.soup.find('div', class_ = ' zm-editable-content clearfix')
        soup = BeautifulSoup('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"></head><body></body></html>')
        soup.body.append(content)

        for noscript in soup.find_all('noscript'):
            noscript.extract()
        for icon in soup.find_all("i", class_='icon-external'):
            icon.extract()
        for img in soup.find_all('img'):
            if img.has_attr('data-actualsrc'):
                img['src'] = "http://" + img['data-actualsrc'][2:]
            elif img.has_attr('eeimg'):
                img['src'] = "http://" + img['src'][2:]

        return soup.prettify()
        content = soup.prettify()

    def save_content(self):
        """ Save answer content into local files, only support html currently. """
        filename = self.eid.split('/')[-1] + ".html"
        with open(filename, 'wb') as f:
            f.write(self.get_content().encode('utf-8'))

    # TODO #

    def get_comments(sefl):
        """ """
