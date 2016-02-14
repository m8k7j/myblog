from django.contrib import admin

# Register your models here.
from blog.models import Author,Tag,Blog

class AuthorAdmin(admin.ModelAdmin):
	list_display=('name','email','website')
	search_field=('name')

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title','author','date_time')
	list_filter = ('date_time',)
	date_hierarchy = 'date_time'
#	ordering = ('-date_time',)
	filter_horizontal=('tags',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Tag)
