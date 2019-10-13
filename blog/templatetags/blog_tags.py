#!/usr/bin/env python
# coding=utf-8
import re
from ..models import Blog, Tag
from django import template
from django.utils.safestring import mark_safe
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_recent_blogs(num=5):
    return Blog.objects.all()[:num]


@register.simple_tag
def get_tags():
    return Tag.objects.exclude(tag_name='private').annotate(num_posts=Count('blog'))

@register.simple_tag
def get_tag_blogs(id):
    tag = Tag.objects.get(id=id)
    return Blog.objects.filter(tags=tag)

@register.simple_tag
def archives():
    return Blog.objects.dates('date_time','year', order='DESC')


@register.simple_tag
def archives_num(year):
    return Blog.objects.filter(date_time__year=year).count()


@register.simple_tag
def get_blog_summary(id):
    blog = Blog.objects.get(id=id)
    content = blog.content
    p1 = ur"(?<=\>).*?(?=\s\s\s)"
    try:
        summary = re.findall(p1, content)[0]
    except:
        summary = 'summary'
    return mark_safe(summary)

