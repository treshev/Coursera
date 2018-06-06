from django.conf.urls import url

from .views import db_create, db_edit_all, db_unsubscribe_u2_from_blogs, db_delete_all, db_get_topic_created_grated, \
    db_get_topic_title_ended, db_get_user_with_limit, db_get_topic_count, db_get_avg_topic_count, db_get_topic_by_u1, \
    db_get_user_that_dont_have_blog, db_get_topic_that_like_all_users, db_get_topic_that_dont_have_like, \
    db_blog_that_have_more_than_one_topic

urlpatterns = [
    url(r'^create/$', db_create),
    url(r'^edit_all/$', db_edit_all),
    url(r'^unsubscribe/$', db_unsubscribe_u2_from_blogs),
    url(r'^delete_all/$', db_delete_all),
    url(r'^get_topic/$', db_get_topic_created_grated),
    url(r'^get_end_topic/$', db_get_topic_title_ended),
    url(r'^get_users/$', db_get_user_with_limit),
    url(r'^get_books/$', db_get_topic_count),
    url(r'^get_avg/$', db_get_avg_topic_count),

    url(r'^get_blog_w_topic/$', db_blog_that_have_more_than_one_topic),
    url(r'^get_topic_by_ul/$', db_get_topic_by_u1),
    url(r'^get_user_blog/$', db_get_user_that_dont_have_blog),
    url(r'^get_topic_like/$', db_get_topic_that_like_all_users),
    url(r'^get_topic_no_like/$', db_get_topic_that_dont_have_like),

]
