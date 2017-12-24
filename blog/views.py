# coding:utf-8
from django.shortcuts import render, render_to_response
from django.views.generic import ListView
import markdown
# Create your views here.
from blog.models import Blog, Tag, Author
from django.http import HttpResponse, Http404, HttpResponse, HttpResponseRedirect
import django_comments
import os
import json
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.syndication.views import Feed


def index(request):
    blogs = Blog.objects.all()
    blogs_list = list(blogs)
    tag_private = Tag.objects.get(tag_name='private')
    blogs_private = tag_private.blog_set.all()
    blogs_private_list = list(blogs_private)
    blogs_public = []
    for blog in blogs_list:
        if blog not in blogs_private_list:
            blogs_public.append(blog)
    tags = Tag.objects.all()
    tags_public = Tag.objects.exclude(tag_name='private')
    user = request.session.get('username')
    if user == 'terry':
        paginator = Paginator(blogs, 5)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        blog_list = current_page.object_list
        print current_page.paginator.num_pages
        print blog_list
        return render_to_response('index.html', {'blog_list': blog_list,
                                                 'tags': tags,
                                                 'username': user,
                                                 'current_page': current_page})
    else:
        paginator = Paginator(blogs_public, 5)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        blog_list = current_page.object_list
        print current_page.paginator.num_pages
        print blog_list
        return render_to_response(
            'index.html',
            {'blog_list': blog_list, 'tags': tags_public, 'username': user,
             'current_page': current_page,
            })


def detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
        tags = blog.tags.all()
        blog_content = markdown.markdown(blog.content,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                             ])
    except Blog.DoesNotExist:
        raise Http404
    return render_to_response('detail.html', {'blog': blog,
                                              'blog_content': blog_content,
                                              'tags': tags, })


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
    blog_pic = request.POST.get('blog_pic')
    tag_name_string = request.POST.get('tags')
    tag_name_list = tag_name_string.split(',')
    tags = Tag.objects.all()
    for tag_name in tag_name_list:
        for tag in tags:
            if tag_name == tag.tag_name:
                break
        else:
            Tag.objects.create(tag_name=tag_name)
    blog = Blog.objects.create(title=title,
                               author=author,
                               content=content,
                               blog_pic=blog_pic,
                               )
    for tag_name in tag_name_list:
        blog.tags.add(Tag.objects.get(tag_name=tag_name))
    id = Blog.objects.order_by('-date_time')[0].id
    return HttpResponseRedirect('/blog/%s' % id)

# uploadImg


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def save_file(path, file_name, data):
    if data is None:
        return
    mkdir(path)
    if(not path.endswith("/")):
        path = path+"/"
    file = open(path+file_name, "wb")
    file.write(data)
    file.flush()


def uploadImg(request):
    if request.method == 'POST':
        file_obj = open("log.txt", "w+")
        buf = request.FILES.get('file', None)
        print >> file_obj, str(buf)
        file_buff = buf.read()
        time_format = str(time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))
        file_name = "img"+time_format+".jpg"
        save_file(
            "/home/terryding/myblog/blog/static/image",
            file_name,
            file_buff)
        dict_tmp = {}
        dict_tmp['error'] = 0
        dict_tmp['url'] = "/static/image/"+file_name
        return HttpResponse(json.dumps(dict_tmp))


def sub_comment(request):
    blog_id = request.POST.get('blog_id')
    comment = request.POST.get('comment_content')
    django_comments.models.Comment.objects.create(
            content_type_id=9,
            object_pk=blog_id,
            site_id=1,
            user=request.user,
            comment=comment,
    )
    return HttpResponseRedirect('/blog/%s' % blog_id)


def tag_blog(request, id):
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    blog_list = current_page.object_list
    return render_to_response('index.html', {'blog_list': blog_list,
                                             'tag': tag,
                                             'current_page': current_page})


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
            paginator = Paginator(blogs, 3)
            page = request.GET.get('page')
            try:
                current_page = paginator.page(page)
            except PageNotAnInteger:
                current_page = paginator.page(1)
            blog_list = current_page.object_list
            return render_to_response(
                'index.html',
                {'blog_list': blog_list, 'tags': tags,
                 'current_page': current_page, 'username': username, })
        else:
            return render_to_response(
                'login.html', {
                    'login_error': "wrong username or password"})
    except BaseException:
        return render_to_response('login.html',
                                  {'login_error': "wrong username or password"})


def update(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except BaseException:
        raise Http404
    user = request.session.get('username')
    if user == 'terry':
        if blog:
            title = blog.title
            tags = blog.tags.all()
            blog_pic = blog.blog_pic
            tag_str = ""
            tag_name = ""
            for tag in tags:
                tag_str = tag_str+str(tag.tag_name)+','
            for i in range(len(tag_str)-1):
                tag_name = tag_name+tag_str[i]
            content = blog.content
            return render_to_response('update.html', {'title': title,
                                                      'content': content,
                                                      'tag_name': tag_name,
                                                      'blog_pic': blog_pic,
                                                      'id': id, })
    else:
        return HttpResponseRedirect('/blog/')


def delete(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except BaseException:
        raise Http404
    user = request.session.get('username')
    if user == 'terry':
        if blog:
            blog.delete()
            return HttpResponseRedirect('/blog/')
    else:
        return HttpResponseRedirect('/blog/')


def blog_update(request, id):
    content = request.POST.get('content')
    author = Author.objects.get(name='terry')
    title = request.POST.get('title')
    blog_pic = request.POST.get('blog_pic')
    tag_name_string = request.POST.get('tags')
    tag_name_list = tag_name_string.split(',')
    tags = Tag.objects.all()
    for tag_name in tag_name_list:
        for tag in tags:
            if tag_name == tag.tag_name:
                break
        else:
            Tag.objects.create(tag_name=tag_name)
    blog = Blog.objects.get(id=id)
    blog.delete()
    blog = Blog.objects.create(title=title,
                               author=author,
                               content=content,
                               blog_pic=blog_pic,
                               )
    for tag_name in tag_name_list:
        blog.tags.add(Tag.objects.get(tag_name=tag_name))
    id = Blog.objects.order_by('-date_time')[0].id
    return HttpResponseRedirect('/blog/%s' % id)


class RSSFeed(Feed):
    title = "RSS Feed - blog"
    link = "terryding.pythonanywhere.com/blog/"
    description = "Rss Feed - blog posts"

    def items(self):
        return Blog.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return "//terryding.pythonanywhere.com/blog/"+str(item.id)+"/"


class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blog_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super(IndexView, self).get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        print (is_paginated)

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3)
                              if(page_number - 3) > 0 else 0: page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3)
                              if(page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data
