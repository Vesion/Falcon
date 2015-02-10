# -*- coding: utf-8 -*-

from zhihu.Session import Session
from zhihu.Question import Question
from zhihu.User import User
from zhihu.Collection import Collection
from zhihu.Answer import Answer
from zhihu.Topic import Topic

if __name__ == "__main__":
    s = Session()
    if s.login():

        q = Question(s, "/question/28033120")
        print q.get_id()
        print q.get_title()
        print q.get_num_answers()
        print q.get_description()
        ts = q.get_topics()
        print ts.next()
        ans = q.get_answers()
        print ans.next()

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
        print c.get_creator()

        a = Answer(s, "/question/28090214/answer/39367455")
        print a.get_id()
        print a.get_author()
        print a.get_num_upvotes()
        print a.get_num_comments()

        t = Topic(s, "/topic/19562033")
        print t.get_id()
        print t.get_num_followers()
        print t.get_description()

    s.logout()