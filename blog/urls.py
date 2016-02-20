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
	url(r'^login/$', views.login,name='login'),
	url(r'^acc_login/$', views.acc_login,name='acc_login'),
	url(r'^update(?P<id>(\d+))/$', views.update, name='update'),
	url(r'^delete(?P<id>(\d+))/$', views.delete, name='delete'),
	url(r'^blog_update(?P<id>(\d+))/$', views.blog_update, name='blog_update'),
]
