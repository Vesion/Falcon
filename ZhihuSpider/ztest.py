# -*- coding: utf-8 -*-

from zhihu.Session import Session
from zhihu.Question import Question

if __name__ == "__main__":
    s = Session()
    s.login()
    q = Question(s, "http://www.zhihu.com/question/28033120")
    print q.get_title()
    print q.get_num_answers()
    print q.get_description()