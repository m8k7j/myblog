#!/usr/bin/env python
# coding=utf-8

from ..models import Blog, Tag
from django import template

register = template.Library()


@register.simple_tag
def get_recent_blogs(num=5):
    return Blog.objects.all()[:num]


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def archives():
    return Blog.objects.dates('date_time', 'month', order='DESC')

