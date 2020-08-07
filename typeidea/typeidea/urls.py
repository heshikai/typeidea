"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.sitemaps import views as sitemap_views

from config.views import links
from .custom_site import custom_site
from blog.views import (
    post_list,post_detail,
    IndexView,CategoryView,TagView,PostDetailView,
    SearchView,AuthorView,
)
from config.views import LinkListView
from comment.views import CommentView                        
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

urlpatterns = [
    path('',IndexView.as_view(),name="index"),
    #path('post/',post_list,name="index"),
    path('post/',IndexView.as_view(),name="index"),
    url(r'category/(?P<category_id>\d+)/$',CategoryView.as_view(),name="category-list"),
    url(r'tag/(?P<tag_id>\d+)/',TagView.as_view(),name="tag-list"),
    url(r'author/(?P<author_id>\d+)/',AuthorView.as_view(),name="author-list"),
    #url(r'post/(?P<post_id>\d+).html/',post_detail,name="post-detail"),
    url(r'post/(?P<post_id>\d+).html',PostDetailView.as_view(),name="post-detail"),
    url(r'post/(?P<post_id>\d+)',PostDetailView.as_view(),name="post-detail"),
    url(r'search/$',SearchView.as_view(),name="search"),
    url(r'^comment/$',CommentView.as_view(),name="comment"),
    url(r'^rss|feed/',LatestPostFeed(),name='rss'),
    url(r'^sitemap\.xml$',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
    path('links/',LinkListView.as_view(),name="links"),
    path('super_admin/',admin.site.urls,name="super-admin"),
    path('admin/', custom_site.urls,name="admin"),
]
