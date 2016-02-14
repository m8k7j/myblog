from django.conf.urls import patterns, include, url

from django.contrib import admin

from blog import views

urlpatterns =[
	url(r'^$', views.index, name='index'),
	url(r'^(?P<id>(\d+))/$', views.detail, name='detail'),
	url(r'^post/$', views.post, name='post'),
	url(r'^blog_add/$', views.blog_add, name='blog_add'),
	url(r'^uploadImg/$', views.uploadImg,name='uploadImg'),
	url(r'^sub_comment/$', views.sub_comment,name='sub_comment'),
	url(r'^tag_blog(?P<id>(\d+))/$', views.tag_blog,name='tag_blog'),
]
