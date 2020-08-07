from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.

from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import CommentForm

class CommentView(TemplateView):
    http_method_names=['post']
    template_name = 'comment/result.html'
    def post(self,request,*args,**kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        #target=request.path

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.owner = User.objects.get(id=1)
            #instance.status = 3
            instance.save()
            succeed=True
            return redirect(target)
        else:
            succeed=False
        
        context = {
            'succeed':succeed,
            'form':comment_form,
            'target':target,
        }

        return self.render_to_response(context)