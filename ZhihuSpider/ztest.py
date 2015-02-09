# -*- coding: utf-8 -*-

from zhihu.Session import Session
from zhihu.Question import Question
from zhihu.User import User
from zhihu.Collection import Collection
from zhihu.Answer import Answer

if __name__ == "__main__":
    s = Session()
    s.login()

    q = Question(s, "/question/28033120")
    print q.get_title()
    print q.get_num_answers()
    print q.get_description()
    ts = q.get_in_topics()
    for i in ts:
        print i

    u = User(s, "/people/yue-shui")
    print u.get_id()
    print u.get_name()
    print u.get_num_followers()
    print u.get_num_followees()
    print u.get_num_agrees()
    print u.get_num_answers()
    print u.get_num_asks()
    print u.get_num_thanks()

    c = Collection(s, "/collection/36750683")
    print c.get_id()
    print c.get_title()
    print c.get_creator().get_name()

    a = Answer(s, "/question/27967203/answer/38917501")
    print a.get_id()
    print a.get_author().get_name()
    print a.get_num_upvotes()
    print a.get_num_comments()

    s.logout()