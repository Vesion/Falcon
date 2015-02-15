# -*- coding: utf-8 -*-

from falcon import Session, Answer, Question, User, Collection, Topic

if __name__ == "__main__":
    s = Session()
    if s.login():

        #q = Question(s, "/question/27936593")
        #print q.getId()
        #print q.get_title()
        #print q.get_num_answers()
        #print q.get_description()
        #print q.get_topics()
        #print q.get_related_questions()
        #print q.get_all_answers(limit = 21)
        #print q.get_all_followers(limit = 21)

        u = User(s, "/people/wonderful-vczh")
        print u.getId()
        print u.get_name()
        print u.get_biography()
        print u.get_about()['education-extra']['text']
        print u.get_num_followers()
        print u.get_num_followees()
        print u.get_num_agrees()
        print u.get_num_answers()
        print u.get_num_asks()
        print u.get_num_thanks()
        print u.get_all_answers(limit = 21)
        print u.get_all_asks(limit = 21)
        print u.get_all_followees(limit = 21)
        print u.get_all_followers(limit = 21)

        #c = Collection(s, "/collection/36750683")
        #print c.getId()
        #print c.get_title()
        #print c.get_creator()

        #a = Answer(s, "/question/28090214/answer/39367455")
        #print a.getId()
        #print a.get_author()
        #print a.get_num_upvotes()
        #print a.get_num_comments()
        #print a.get_text_content()

        #t = Topic(s, "/topic/19562033")
        #print t.getId()
        #print t.get_num_followers()
        #print t.get_description()

    s.logout()