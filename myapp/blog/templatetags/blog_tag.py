from django import template
from ..models import Post, Comment
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag
def last_post_date():
    return Post.published.last().publish

# @register.simple_tag
# def post_most_reading_time():
#     c = float('inf')
#     for i in Post.published.all():
#         if i.reading_time < c:
#             c = i.reading_time
#     return (f'{Post.published.filter(reading_time=c)[0].reading_time}پست با بیشترین زمان مورد نیاز برای مطالعه و '
#             f'{Post.published.filter(reading_time=c)[0].reading_time}زمان مورد نیاز برای مطالعه این پست : ')


@register.simple_tag
def post_most_reading_time():
    c = 0
    for i in Post.published.all():
        if i.reading_time > c:
            c = i.reading_time
    return Post.published.filter(reading_time=c)[0].title


@register.simple_tag
def most_reading_time():
    c = 0
    for i in Post.published.all():
        if i.reading_time > c:
            c = i.reading_time
    return Post.published.filter(reading_time=c)[0].reading_time


@register.simple_tag
def post_least_reading_time():
    c = float('inf')
    for i in Post.published.all():
        if i.reading_time < c:
            c = i.reading_time
    return Post.published.filter(reading_time=c)[0].title


@register.simple_tag
def least_reading_time():
    c = float('inf')
    for i in Post.published.all():
        if i.reading_time < c:
            c = i.reading_time
    return Post.published.filter(reading_time=c)[0].reading_time


@register.simple_tag
def most_popular_post(count=5):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]


@register.simple_tag
def most_active_user():
    return User.objects.annotate(active_user=Count('user_posts')).order_by('-active_user')


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=1):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context


@register.filter()
def to_markdown(text):
    return mark_safe(markdown(text))


@register.filter()
def word_filtering(word, arg):
    return mark_safe(word.replace(arg, '****'))
