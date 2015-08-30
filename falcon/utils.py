#  ________      ______                   
#  ___  __/_____ ___  /__________________ 
#  __  /_ _  __ `/_  /_  ___/  __ \_  __ \
#  _  __/ / /_/ /_  / / /__ / /_/ /  / / /
#  /_/    \__,_/ /_/  \___/ \____//_/ /_/ 
#                              
# Author : Shine Xu
# License: The MIT License (MIT)

# -*- coding: utf-8 -*-

#
# MODULES
#

## Modules for common use 
import os
import sys
import platform
import shutil
import json
import re

## Module for HTTP requests
import requests

## Module for HTML parsing, try to use lxml engine
from bs4 import BeautifulSoup as BS
try:
    __import__('lxml')
    BeautifulSoup = lambda makeup: BS(makeup, 'lxml')
except ImportError:
    BeautifulSoup = lambda makeup: BS(makeup, 'html.parser')

#
# CONSTANTS
#

## Status Code
SUCCESS = 1
FAILURE = 0

## Encoding
CODE = "gbk" if platform.system() == "Windows" else\
        "utf-8"

## URLs
HOST_URL = "http://www.zhihu.com"
### Session
Login_URL = HOST_URL + "/login/email"
Logout_URL = HOST_URL + "/logout"
Get_Captcha_URL = HOST_URL + "/captcha.gif"
### Home
Get_FQ_URL = HOST_URL + "/question/following"
Get_More_FQ_URL = HOST_URL + "/node/ProfileFollowedQuestionsV2"
Get_FC_URL = HOST_URL + "/collections"
Get_More_FC_URL = Get_FC_URL
### Collection
Follow_Collection_URL = HOST_URL + "/collection/follow"
Unfollow_Collection_URL = HOST_URL + "/collection/unfollow"
### User
Get_More_Followees_URL = HOST_URL + "/node/ProfileFolloweesListV2"
Get_More_Followers_URL = HOST_URL + "/node/ProfileFollowersListV2"
Follow_User_URL = HOST_URL + "/node/MemberFollowBaseV2"
Unfollow_User_URL = Follow_User_URL
### Topic
Follow_Topic_URL = HOST_URL + "/node/TopicFollowBaseV2"
Unfollow_Topic_URL = Follow_Topic_URL
### Question
Get_More_Answers_URL = HOST_URL + "/node/QuestionAnswerListV2"
Get_Collapsed_Answers_URL = HOST_URL + "/node/QuestionCollapsedAnswerListV2"
Follow_Question_URL = HOST_URL + "/node/QuestionFollowBaseV2"
Unfollow_Question_URL = Follow_Question_URL
### Answer
Vote_Neutral_Answer_URL = HOST_URL + "/node/AnswerVoteBarV2"
Vote_Up_Answer_URL = Vote_Neutral_Answer_URL
Vote_Down_Answer_URL = Vote_Neutral_Answer_URL

#Column_URL = "http://zhuanlan.zhihu.com"
#Columns_Data = Column_URL + '/api/columns/{0}'
#Columns_Posts_Data = Column_URL + '/api/columns/{0}/posts?limit=10&offset={1}'
#Columns_Post_Data = Column_URL + '/api/columns/{0}/posts/{1}'

## REs
Eid_RE = re.compile(r"^(/[^/]+)*$")
Number_RE = re.compile(r'[^\d]*(\d+).*')

## Numbers
Page_Items_Num = 20 # Define the number when getting the items firstly, this also defines the offset of more items post request with AJAX.
Page_Answers_Num = 50 # Used in Question

#
# FUNCTIONS
#

def get_all_(gen):
    """ An advanced fucntion using generator to get all entry eids. """
    i = gen()
    eids = []
    try:
        while True:
            eids.append(i.next())
    except StopIteration: pass
    finally:
        return eids

## DECORATORS
import functools

def check_eid(func):
    """ When an entry initiating, check its eid whether valid. """
    @functools.wraps(func)
    def wrapper(self, session, eid = ''):
        if eid and Eid_RE.match(eid) is None:
            raise ValueError('eid value error')
        return func(self, session, eid)
    return wrapper

def return_int(func):
    """ Match number from string, return int. """
    @functools.wraps(func)
    def wrapper(self):
        text = func(self)
        num = Number_RE.match(text)
        if num:
            return int(num.group(1))
        return 0
    return wrapper

