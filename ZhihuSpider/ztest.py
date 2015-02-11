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

        q = Question(s, "/question/27936593")
        print q.get_id()
        print q.get_title()
        print q.get_num_answers()
        print q.get_description()
        ts = q.get_topics()
        #ans = q.get_answers()
        #for i in xrange(0, q.get_num_answers()):
        #    print "{0} : {1}".format(i+1, ans.next())
        fs = q.get_followers()
        for i in xrange(0, q.get_num_followers()):
            print "{0} : {1}".format(i+1, fs.next())
        #rqs = q.get_related_questions()

        #u = User(s, "/people/yue-shui")
        #print u.get_id()
        #print u.get_name()
        #print u.get_num_followers()
        #print u.get_num_followees()
        #print u.get_num_agrees()
        #print u.get_num_answers()
        #print u.get_num_asks()
        #print u.get_num_thanks()

        #c = Collection(s, "/collection/36750683")
        #print c.get_id()
        #print c.get_title()
        #print c.get_creator()

        #a = Answer(s, "/question/28090214/answer/39367455")
        #print a.get_id()
        #print a.get_author()
        #print a.get_num_upvotes()
        #print a.get_num_comments()

        #t = Topic(s, "/topic/19562033")
        #print t.get_id()
        #print t.get_num_followers()
        #print t.get_description()

    s.logout()