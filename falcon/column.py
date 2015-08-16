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

class Column(Entry):
    """ Tool class for getting column info """

    _cHOST_ = "http://zhuanlan.zhihu.com/"

    def __init__(self, session, url):
        self.session = requests.session()
        self.url = url

        self.soup = BeautifulSoup(self.session.get(Column._cHOST_ + self.url).content)

    def get_title(self):
        title = self.soup.find('div', class_ = 'title ng-binding')\
                        .string.encode('utf-8').strip('\n')
        return self.encode2Character(title)

    #def get_num_followers(self):
