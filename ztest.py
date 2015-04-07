# -*- coding: utf-8 -*-

from falcon import Session, Home, Answer, Question, User, Collection, Topic, Column

if __name__ == "__main__":
    s = Session()
    if s.login():

        i = Home(s)
        print i.get_all_following_questions(limit = 22)

        q = Question(s, "/question/27936593")
        print q.getId()
        print q.get_title()
        print q.get_num_answers()
        print q.get_description()
        print q.get_topics()
        print q.get_related_questions()
        print q.get_all_answers(limit = 21)
        print q.get_all_followers(limit = 21)
        print ''

        u = User(s, "/people/fu-er")
        print u.getId()
        print u.get_name()
        print u.get_biography()
        print u.get_about()['business']['text']
        print u.get_num_followers()
        print u.get_num_followees()
        print u.get_num_agrees()
        print u.get_num_answers()
        print u.get_num_asks()
        print u.get_num_thanks()
        print u.get_num_column_papers()
        print u.get_all_answers(limit = 21)
        print u.get_all_asks(limit = 21)
        print u.get_all_followees(limit = 21)
        print u.get_all_followers(limit = 21)
        print ''

        c = Collection(s, "/collection/36750683")
        print c.getId()
        print c.get_title()
        print c.get_creator()
        print ''

        a = Answer(s, "/question/28090214/answer/39367455")
        print a.getId()
        print a.get_author()
        print a.get_num_upvotes()
        print a.get_num_comments()
        print a.get_num_collects()
        print a.get_text_content()
        print ''

        t = Topic(s, "/topic/19562033")
        print t.getId()
        print t.get_num_followers()
        print t.get_description()
        print ''


    s.logout()