from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView,ListView
from django.db.models import Q,F
from django.contrib.auth.models import User

from datetime import date
from django.core.cache import cache

from .models import Category,Tag,Post
from config.models import SideBar
from comment.models import Comment
from comment.forms import CommentForm
# Create your views here.

def post_list(request,category_id=None,tag_id = None):
    '''content = 'post_list category_id={category_id},tag_id={tag_id}'.format(
        category_id = category_id,
        tag_id = tag_id,
    )

    return HttpResponse(content)'''
    tag = None
    category = None

    post_list = Post.objects.filter(status = Post.STATUS_NORMAL)
    if tag_id:
        post_list,tag  = Post.get_by_tag(tag_id)
    elif category_id:
        post_list,category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request,'blog/list.html',context = context)

def post_detail(request,post_id):
    #return HttpResponse('detail')
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    
    context = {
        'post':post,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request,'blog/detail.html',context = context)


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars':SideBar.get_all(),}) 
        context.update(Category.get_navs())
        context.update({'tags':Tag.get_all(),})
        return context
    
class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list' #如果不设置此项，在模板中需要使用object_list 作为常量
    template_name = 'blog/list.html'

class IndexView(CommonViewMixin,PostListView):
    pass

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({'category':category})
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update({'tag':tag})
        return context

    def get_queryset(self):
        """重写queryset，根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)

class PostDetailView(CommonViewMixin,DetailView):
    queryset=Post.latest_posts()
    template_name = "blog/detail.html"
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.get_by_target(self.request.path)
        context.update({
            'comment_form':CommentForm,
            'comments':comments,
        })
        return context
    
    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid,self.request.path)
        uv_key = 'uv:%s:%s:%s' % (
                uid,str(date.today()),self.request.path
            )
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key,1,1*60)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key,1,24*60*60)
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(
                pv=F('pv')+1,uv=F('uv')+1 )
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)


    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.handle_visited()
        '''Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)

        #调试用
        from django.db import connection
        print(connection.queries)'''
        return response
    #model = Post
    #template_name = 'blog/detail.html'

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(
            Q(title__icontains=keyword)|Q(desc__icontains=keyword)
        )

class AuthorView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        author_id = self.kwargs.get('author_id')
        context.update({
            'author':User.objects.get(id=author_id)
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('author_id')
        if not author_id:
            return queryset
        return queryset.filter(owner_id=author_id)