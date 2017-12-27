from django.conf.urls import include, url

from django.contrib import admin

from blog import views

from blog.views import RSSFeed

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog/$', views.index, name='index'),
    url(r'^blog/(?P<id>(\d+))/$', views.detail, name='detail'),
    url(r'^post/$', views.post, name='post'),
    url(r'^blog_add/$', views.blog_add, name='blog_add'),
    url(r'^uploadImg/$', views.uploadImg, name='uploadImg'),
    url(r'^sub_comment/$', views.sub_comment, name='sub_comment'),
    url(r'^tag_blog/(?P<id>(\d+))/$', views.tag_blog, name='tag_blog'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^login/$', views.login, name='login'),
    url(r'^acc_login/$', views.acc_login, name='acc_login'),
    url(r'^update(?P<id>(\d+))/$', views.update, name='update'),
    url(r'^delete(?P<id>(\d+))/$', views.delete, name='delete'),
    url(r'^blog_update(?P<id>(\d+))/$', views.blog_update, name='blog_update'),
    url(r'^feed/$', RSSFeed(), name='RSS'),
]
