from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegistrationsForm
from django.contrib.auth.forms import AuthenticationForm #add this
from blog.models import *
from .forms import TagForm

# Create your views here.
template_location='base/dashboard/'

def registrations_views(request):
    template    = template_location+'registrations.html'
    if request.method == "POST":
	    form = RegistrationsForm(request.POST)
	    if form.is_valid():
		    user = form.save()
		    login(request, user)
		    messages.success(request, "Registration successful." )
		    return redirect("login")
	    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationsForm()
    context={
        "register_form":form,
        }
    return render (request,template,context)

def login_view(request):
    template    = template_location+'login.html'
    if request.method == "POST":
	    form = AuthenticationForm(request, data=request.POST)
	    if form.is_valid():
		    username = form.cleaned_data.get('username')
		    password = form.cleaned_data.get('password')
		    user = authenticate(username=username, password=password)
		    if user is not None:
		    	login(request, user)
		    	messages.info(request, f"You are now logged in as {username}.")
		    	return redirect("post-list")
		    else:
		    	messages.error(request,"Invalid username or password.")
	    else:
		    messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context={
        "login_form":form,
        }
    return render(request,template,context)

def logout_view(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

def tag_create_view(request):
    template    = template_location+'tag-create.html'
    if request.method == 'POST':
        forms = TagForm(request.POST)
        if forms.is_valid():
            forms.save()
            forms = TagForm()
    else:
        forms = TagForm()
    context={
        "form":forms
    }
    return render(request,template,context)
