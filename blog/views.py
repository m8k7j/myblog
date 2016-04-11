from django.shortcuts import render,render_to_response

# Create your views here.
from blog.models import Blog,Tag, Author
from django.http import HttpResponse, Http404, HttpResponse,HttpResponseRedirect
import django_comments
import os,json,time
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.syndication.views import Feed

def index(request):
	blogs = Blog.objects.all()
        blogs_list = list(blogs)
        tag_private = Tag.objects.get(tag_name='private')
        blogs_private = tag_private.blog_set.all()
        blogs_private_list = list(blogs_private)
        for blog in blogs_list:
            for blog_private in blogs_private_list:
                if blog==blog_private:
                    blogs_list.remove(blog)
        blogs_public = blogs_list
	tags = Tag.objects.all()
        tags_public = Tag.objects.exclude(tag_name='private')
        user = request.session.get('username')
        if user == 'terry':
	    paginator =Paginator(blogs,3)
	    page = request.GET.get('page')
	    try:
		current_page = paginator.page(page)
	    except PageNotAnInteger:
		current_page = paginator.page(1)
	    blog_list = current_page.object_list
	    print current_page.paginator.num_pages
	    print blog_list
	    return render_to_response('index.html',{'blog_list':blog_list,
											'tags': tags,
											'current_page':current_page})
        else:
	    paginator = Paginator(blogs_public,3)
	    page = request.GET.get('page')
	    try:
		current_page = paginator.page(page)
	    except PageNotAnInteger:
		current_page = paginator.page(1)
	    blog_list = current_page.object_list
	    print current_page.paginator.num_pages
	    print blog_list
	    return render_to_response('index.html',{'blog_list':blog_list,
											'tags': tags_public,
											'current_page':current_page})
def detail(request,id):
	try:
		blog = Blog.objects.get(id=id)
		tags = blog.tags.all()
	except Blog.DoesNotExist:
		raise Http404
	return render_to_response('detail.html',{'blog':blog,
											 'tags':tags,})

def post(request):
	user = request.session.get('username')
	if user == 'terry':
		return render_to_response('post.html')
	else:
		return HttpResponseRedirect('/blog/')
		
											 
def blog_add(request):
	content = request.POST.get('content')
	author = Author.objects.get(name='terry')
	title = request.POST.get('title')
	tag_name_string= request.POST.get('tags')
	tag_name_list = tag_name_string.split(',')
	tags = Tag.objects.all()
	for tag_name in tag_name_list:
		for tag in tags:
			if tag_name==tag.tag_name:
				break
		else:
			Tag.objects.create(tag_name=tag_name)
	blog=Blog.objects.create(title=title,
						author=author,
						content=content,
						)
	for tag_name in tag_name_list:
		blog.tags.add(Tag.objects.get(tag_name=tag_name))
	id= Blog.objects.order_by('-date_time')[0].id
	return HttpResponseRedirect('/blog/%s' %id)

#uploadImg
def mkdir(path):
	path = path.strip()
	path = path.rstrip("\\")
	if not os.path.exists(path):
		os.makedirs(path)
	return path

def save_file(path, file_name, data):
	if data == None:
		return
	mkdir(path)
	if(not path.endswith("/")):
		path=path+"/"
	file = open(path+file_name,"wb")
	file.write(data)
	file.flush()

def uploadImg(request):
	if request.method=='POST':
		file_obj = open("log.txt","w+")
		buf = request.FILES.get('file',None)
		print >> file_obj, str(buf)
		file_buff = buf.read()
		time_format=str(time.strftime("%Y-%m-%d-%H%M%S",time.localtime()))
		file_name = "img"+time_format+".jpg"
		save_file("/home/terryding/myblog/blog/static/image", file_name,file_buff)
		dict_tmp = {}
		dict_tmp['error']=0
		dict_tmp['url']="/static/image/"+file_name
		return HttpResponse(json.dumps(dict_tmp))

def sub_comment(request):
	blog_id = request.POST.get('blog_id')
	comment=request.POST.get('comment_content')
	django_comments.models.Comment.objects.create(
		content_type_id=9,
		object_pk=blog_id,
		site_id=1,
		user=request.user,
		comment=comment,
	)
	return HttpResponseRedirect('/blog/%s' %blog_id)

def tag_blog(request,id):
	tag = Tag.objects.get(id=id)	
	blogs = tag.blog_set.all()
	paginator = Paginator(blogs,3)
	page = request.GET.get('page')
	try:
		current_page = paginator.page(page)
	except PageNotAnInteger:
		current_page = paginator.page(1)
	blog_list = current_page.object_list
	return render_to_response('index.html',{'blog_list':blog_list,
											'tag': tag,
											'current_page':current_page})
def login(request):
	return render_to_response('login.html')

def acc_login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	try:
		author = Author.objects.get(name=username)
		if password == author.password:
			request.session['username'] = username
			blogs = Blog.objects.all()
			tags = Tag.objects.all()
			paginator = Paginator(blogs,3)
			page = request.GET.get('page')
			try:
				current_page = paginator.page(page)
			except PageNotAnInteger:
				current_page = paginator.page(1)
			blog_list = current_page.object_list
			return render_to_response('index.html',{'blog_list':blog_list,
											'tags': tags,
											'current_page':current_page,
											'username':username,})
		else:
			return render_to_response('login.html',{'login_error': "wrong username or password"})
	except:
		return render_to_response('login.html',{'login_error': "wrong username or password"})

def update(request,id):
	try:
		blog = Blog.objects.get(id=id)
	except:
		raise Http404
	user = request.session.get('username')
	if user == 'terry':
		if blog:
			title = blog.title
			tags = blog.tags.all()
			tag_str=""
			tag_name=""
			for tag in tags:
				tag_str = tag_str+str(tag.tag_name)+','
			for i in range(len(tag_str)-1):
				tag_name = tag_name+tag_str[i]
			content = blog.content
			return render_to_response('update.html',{'title':title,
												 'content':content,
												 'tag_name':tag_name,
												 'id': id,})
	else:
		return HttpResponseRedirect('/blog/')
		
	
def delete(request,id):
	try:
		blog = Blog.objects.get(id=id)
	except:
		raise Http404
	user = request.session.get('username')
	if user == 'terry':
		if blog:
			blog.delete()
			return HttpResponseRedirect('/blog/')
	else:
		return HttpResponseRedirect('/blog/')
		
def blog_update(request,id):
	content = request.POST.get('content')
	author = Author.objects.get(name='terry')
	title = request.POST.get('title')
	tag_name_string= request.POST.get('tags')
	tag_name_list = tag_name_string.split(',')
	tags = Tag.objects.all()
	for tag_name in tag_name_list:
		for tag in tags:
			if tag_name==tag.tag_name:
				break
		else:
			Tag.objects.create(tag_name=tag_name)
        blog = Blog.objects.get(id=id)
        blog.delete()
	blog=Blog.objects.create(title=title,
						author=author,
						content=content,
						)
	for tag_name in tag_name_list:
		blog.tags.add(Tag.objects.get(tag_name=tag_name))
	id= Blog.objects.order_by('-date_time')[0].id
	return HttpResponseRedirect('/blog/%s' %id)

class RSSFeed(Feed):
        title = "RSS Feed - blog"
        link = "/blog/"
        description = "Rss Feed - blog posts"
        def items(self):
            return Blog.objects.order_by('-date_time')
        def item_title(self,item):
            return item.title
        def item_pubdate(self,item):
            return item.date_time
        def item_description(self,item):
            return item.content
        def item_link(self,item):
            return "//terryding.pythonanywhere.com/blog"+str(item.id)+"/"
