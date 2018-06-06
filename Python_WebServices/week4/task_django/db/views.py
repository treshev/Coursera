from django.http import HttpResponse

from .query import create, edit_all, unsubscribe_u2_from_blogs, delete_all, get_topic_created_grated, \
    get_topic_title_ended, get_user_with_limit, get_topic_count, get_avg_topic_count, get_topic_by_u1, \
    get_user_that_dont_have_blog, get_topic_that_like_all_users, get_topic_that_dont_have_like, \
    get_blog_that_have_more_than_one_topic


def db_delete_all(request):
    delete_all()
    return HttpResponse('OK')


def db_create(request):
    create()
    return HttpResponse('OK')


def db_edit_all(request):
    edit_all()
    return HttpResponse('OK')


def db_get_topic_created_grated(request):
    get_topic_created_grated()
    return HttpResponse('OK')


def db_get_topic_created_grated(request):
    get_topic_created_grated()
    return HttpResponse('OK')


def db_unsubscribe_u2_from_blogs(request):
    unsubscribe_u2_from_blogs()
    return HttpResponse('OK')


def db_get_topic_title_ended(request):
    get_topic_title_ended()
    return HttpResponse('OK')


def db_get_user_with_limit(request):
    get_user_with_limit()
    return HttpResponse('OK')


def db_get_topic_count(request):
    get_topic_count()
    return HttpResponse('OK')


def db_get_avg_topic_count(request):
    get_avg_topic_count()
    return HttpResponse('OK')


def db_blog_that_have_more_than_one_topic(request):
    get_blog_that_have_more_than_one_topic()
    return HttpResponse('OK')


def db_get_topic_by_u1(request):
    get_topic_by_u1()
    return HttpResponse('OK')


def db_get_user_that_dont_have_blog(request):
    get_user_that_dont_have_blog()
    return HttpResponse('OK')


def db_get_topic_that_like_all_users(request):
    get_topic_that_like_all_users()
    return HttpResponse('OK')


def db_get_topic_that_dont_have_like(request):
    get_topic_that_dont_have_like()
    return HttpResponse('OK')
