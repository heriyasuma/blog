from django.shortcuts import render
from . models import Post,Categorie,Tag
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from galleries.models import Gallerie
from comments.forms import CommentForm
from comments.models import Comment
from random import choices

# Create your views here.
def theme_dev_view(request):
    return render(request,"base/index.html",{})

def categorie_list():
    queryset_list_categorie    = Categorie.objects.all().order_by("title")
    return queryset_list_categorie

def tag_list():
    queryset_list_tag    = Tag.objects.all().order_by("title")
    return queryset_list_tag

def random_post(q=5):
    rnd = list(Post.objects.all())
    rnd_choices = choices(rnd,k=q)
    return rnd_choices

template_location='base/blog/'

def post_list_view(request):
    template    = template_location+'post-list.html'
    queryset_list   = Post.objects.all().order_by("-timestamp")
    paginator   = Paginator(queryset_list, 3) # Show 25 contacts per page
    page        = request.GET.get('page')
    queryset    = paginator.get_page(page)
    context={
        'objects':queryset,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)

def post_detail_view(request,slug):
    template    = template_location+'post-detail.html'
    instance    = get_object_or_404(Post,slug=slug)

    queryset_gallerie = get_object_or_404(Gallerie,title=instance.thumbnail)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        forms = CommentForm(request.POST or None)
        if forms.is_valid():
           forms.save()
           forms = form.cleaned_data('content')
        else:
            print('method not valid')
    else :
        forms = CommentForm(request.POST or None, initial= initial_data)

    comments =  instance.comments # Comment.objects.filter_by_instance(instance)

    context={
        'instance':instance,
        'objects':queryset_gallerie,
        'comments':comments,
        'form':forms,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)

def categorie_list_view(request):
    template    = template_location+'categorie-list.html'
    queryset_list    = Categorie.objects.all().order_by("-timestamp")
    paginator   = Paginator(queryset_list, 10) # Show 25 contacts per page
    page        = request.GET.get('page')
    queryset    = paginator.get_page(page)
    context={
        'objects':queryset,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)

def categorie_detail_view(request,slug):
    template        = template_location+'categorie-detail.html'
    queryset        = get_object_or_404(Categorie,slug=slug)
    queryset_post   = Post.objects.filter(category=queryset.id).order_by("-timestamp")
    context={
        'instance':queryset,
        'objects':queryset_post,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)

def tag_list_view(request):
    template    = template_location+'tag-list.html'
    queryset_list    = Tag.objects.all().order_by("-timestamp")
    paginator   = Paginator(queryset_list, 10) # Show 25 contacts per page
    page        = request.GET.get('page')
    queryset    = paginator.get_page(page)
    context={
        'objects':queryset,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)

def tag_detail_view(request,slug):
    template    = template_location+'tag-detail.html'
    queryset    = get_object_or_404(Tag,slug=slug)
    queryset_post   = Post.objects.filter(tag=queryset.id).order_by("-timestamp")
    context={
        'instance':queryset,
        'objects':queryset_post,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)

#def search_results_view(request):
#    template    = template_location+'search-results.html'
#    # if this is a POST request we need to process the form data
#    if request.method == 'POST':
#        searched    = request.POST['searched']
#        queryset    = Post.objects.filter(title__contains=searched)
#
#    context={
#        'objects':queryset,
#        'categorie':categorie_list(),
#        'tags': tag_list(),
#        'random_post': random_post(),
#    }
#    return render(request,template,context)

def search_results_view(request):
    template    = template_location+'search-results.html'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        searched    = request.POST['searched']
        queryset    = Post.objects.filter(title__contains=searched)
    else:
        queryset    = Post.objects.all()
    context={
        'objects':queryset,
        'categorie':categorie_list(),
        'tags': tag_list(),
        'random_post': random_post(),
    }
    return render(request,template,context)
