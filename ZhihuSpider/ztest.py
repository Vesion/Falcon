# -*- coding: utf-8 -*-

from zhihu.Session import Session
from zhihu.Question import Question

if __name__ == "__main__":
    s = Session()
    s.login()
    q = Question(s, "http://www.zhihu.com/question/24269892")
    t = q.get_title()
    print t