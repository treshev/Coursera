from django.db.models import Avg
from django.db.models import Count

from .models import User, Blog, Topic


def create():
    u1 = User(first_name='u1', last_name='u1')
    u2 = User(first_name='u2', last_name='u2')
    u3 = User(first_name='u3', last_name='u3')

    u1.save()
    u2.save()
    u3.save()

    '''
    OR
    u1 = User.objects.create(first_name='u1', last_name='u1')
    u2 = User.objects.create(first_name='u2', last_name='u2')
    u3 = User.objects.create(first_name='u3', last_name='u3')
    '''

    blog1 = Blog(title='blog1', author=u1)
    blog2 = Blog(title='blog2', author=u1)
    blog1.save()
    blog2.save()

    '''
    OR
    b1 = Blog.objects.create(title='blog1', author=u1)
    b2 = Blog.objects.create(title='blog2', author=u1)
    '''

    blog1.subscribers.add(u1, u2)
    blog2.subscribers.add(u2)

    topic1 = Topic(title='topic1', blog=blog1, author=u1)
    topic2 = Topic(title='topic2_content', blog=blog1, author=u3, created='2017-01-01')
    topic1.save()
    topic2.save()

    topic1.likes.add(u1, u2, u3)


def delete_all():
    User.objects.all().delete()
    Blog.objects.all().delete()
    Topic.objects.all().delete()


def edit_all():
    for user in User.objects.all():
        user.first_name = 'uu1'
        user.save()

    #or User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    for user in User.objects.filter(first_name__in=['u1', 'u2']):
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    for user in User.objects.filter(first_name='u1'):
        user.delete()
    #or User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    user = User.objects.get(first_name='u2')
    for blog in Blog.objects.filter(subscribers=user):
        print(blog.subscribers.remove(user))
    #Blog.subscribers.through.objects.filter(user__first_name='u2').delete()


# 4. Найти топики у которых дата создания больше 2018-01-01
def get_topic_created_grated():
    return Topic.objects.filter(created__gt='2018-01-01')
    #TODO:Topic.objects.filter(created__gt=datetime(year=2018, month=1, day=1, tzinfo=UTC))


# 5.Найти топик у которого title заканчивается на content
def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


# 6.Получить 2х первых пользователей (сортировка в обратном порядке по id)
def get_user_with_limit():
    return User.objects.all().order_by('-id')[:2]


# 7. Получить количество топиков в каждом блоге, назвать поле topic_count, отсортировать по topic_count по возрастанию (функция get_topic_count).
def get_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')


# 8. Получить среднее количество топиков в блоге (функция get_avg_topic_count).
def get_avg_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(Avg('topic_count'))


# 9. Найти блоги, в которых топиков больше одного (функция get_blog_that_have_more_than_one_topic).
def get_blog_that_have_more_than_one_topic():
    return Blog.objects.all().annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


# 10. Получить все топики автора с first_name u1 (функция get_topic_by_u1).
def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


# 11. Найти пользователей, у которых нет блогов, отсортировать по возрастанию id (функция get_user_that_dont_have_blog).
def get_user_that_dont_have_blog():
    return User.objects.filter(blog__id__isnull=True).order_by('pk')


# 12. Найти топик, который лайкнули все пользователи (функция get_topic_that_like_all_users).
def get_topic_that_like_all_users():
    count = User.objects.all().count()
    return Topic.objects.annotate(like_count=Count('likes')).filter(like_count=count)


# 13. Найти топики, у которо нет лайков (функция get_topic_that_dont_have_like).
def get_topic_that_dont_have_like():
    return Topic.objects.filter(likes__isnull=True)
