
#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

# Packages and modules for common use 
import os
import shutil
import json
import re

# Module for HTTP requests
import requests

# Module for HTML parsing, try to use lxml engine
from bs4 import BeautifulSoup as BS
try:
    __import__('lxml')
    BeautifulSoup = lambda makeup: BS(makeup, 'lxml')
except ImportError:
    BeautifulSoup = lambda makeup: BS(makeup, 'html.parser')

# CONSTANTS
HOST_URL = "http://www.zhihu.com"
Login_URL = HOST_URL + "/login/email"
Logout_URL = HOST_URL + "/logout"
Get_Captcha_URL = HOST_URL + "/captcha.gif"
Get_Profile_Card_URL = HOST_URL + "/node/MemberProfileCardV2"
Get_More_Answer_URL = HOST_URL + "/node/QuestionAnswerListV2"
Get_More_Followers_URL = HOST_URL + "/node/ProfileFollowersListV2"
Get_More_Followees_URL = HOST_URL + "/node/ProfileFolloweesListV2"

Column_URL = 'http://zhuanlan.zhihu.com'
#Columns_Data = Column_URL + '/api/columns/{0}'
#Columns_Posts_Data = Column_URL + '/api/columns/{0}/posts?limit=10&offset={1}'
#Columns_Post_Data = Column_URL + '/api/columns/{0}/posts/{1}'