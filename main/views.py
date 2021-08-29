from django.shortcuts import render
from . models import Blog
from categories.models import *
from posts.models import *
from django.shortcuts import get_object_or_404
# Create your views here.

TEMPLATE_DIR='basic/main/'
def index(request):
    template=TEMPLATE_DIR + 'index.html'
    context={
        'objects':'test',
    }
    return render(request,template,context)

#def blog_categorie_view(request):
#    template=TEMPLATE_DIR + 'blog/categorie-list.html'
#    instance= Blog.objects.get(pk=1)
##    objects = Categorie.objects.filter_by_instance(instance)
#    objects = instance.blog_categories
#    context={
#        'objects':objects,
#    }
#    return render(request,template,context)

#def blog_categorie_view(request,slug):
#    template=TEMPLATE_DIR + 'blog/categorie-list.html'
#    instance= get_object_or_404(Blog, slug=slug)
#    objects = instance.blog_categories
#    context={
#        'objects':objects,
#    }
#    return render(request,template,context)

def blog_categorie_view(request,slug):
    template=TEMPLATE_DIR + 'blog/categorie-list.html'
    instance= get_object_or_404(Blog, slug=slug)
    categorie = instance.blog_categories
    objects = Post.objects.filter(category=1)
    context={
        'objects':objects,
    }
    return render(request,template,context)
