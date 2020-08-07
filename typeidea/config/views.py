from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView
# Create your views here.
from .models import Link

from comment.forms import CommentForm
from comment.models import Comment
from blog.views import CommonViewMixin

def links(request):
    return HttpResponse('links')

class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = "config/links.html"
    context_object_name = 'link_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.get_by_target(self.request.path)
        context.update({
            'comment_form':CommentForm,
            'comments':comments,
        })
        return context
    