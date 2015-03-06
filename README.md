Next generation of Zhihu spider

More APIs being updated.

<h2>API reference</h2>

<h3>Session:</h3>

login()

logout()


<h3>Question:</h3>

get_title(self):

get_description(self):

get_num_answers(self):

get_num_followers(self):

get_topics(self):

get_related_questions(self):

get_answers(self):

get_followers(self):

get_all_answers(self, limit = sys.maxsize):

get_all_followers(self, limit = sys.maxsize):



<h3>User:</h3>

get_name(self):

get_biography(self):

get_about_item(self, name):

get_about(self):

get_num_followees(self):

get_num_followers(self):

get_num_agrees(self):

get_num_thanks(self):

get_num_asks(self):

get_num_answers(self):

get_num_column_papers(self):

get_answers(self):

get_asks(self):

get_followees(self):

get_followers(self):

get_all_answers(self, limit = sys.maxsize):

get_all_asks(self, limit = sys.maxsize):

get_all_followees(self, limit = sys.maxsize):

get_all_followers(self, limit = sys.maxsize):



<h3>Collection:</h3>

get_title()

get_creator()



<h3>Answer:</h3>

get_author()

get_num_upvotes()

get_text_content_text()



<h3>Topic:</h3>

get_num_followers()

get_description()
