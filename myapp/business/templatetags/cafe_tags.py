from django import template
from ..models import Cafe, Comment
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown
from django.core.cache import cache


register = template.Library()


@register.simple_tag()
def total_open_cafes():
    return Cafe.opened.count()


@register.simple_tag()
def total_open_cafes_name():
    for cafe in Cafe.opened.all():
        return cafe


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_cafe_date():
    return Cafe.opened.last().publish


@register.simple_tag
def most_popular_cafes(count=6):
    return Cafe.opened.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]


@register.inclusion_tag('partials/last_cafe.html')
def last_cafes(refresh, count=6):
    if refresh == 'True':
        l_cafes = Cafe.opened.order_by('-publish')[:count]
        cache.set('last_cafes_result', l_cafes, 3600)
        context = {
            'l_cafes': l_cafes
        }
        return context
    elif refresh == 'False':
        l_cafes = cache.get('last_cafes_result')
        cache.set('last_cafes_result', l_cafes, 3600)
    context = {
        'l_cafes': l_cafes
    }
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))
