from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
template_location='base/dashboard/'

def login_view(request):
    template    = template_location+'login.html'
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
                login(request,user)
                return redirect('/')
        else :
            messages.success(request,'success')
            redirect('login')
    else:
        context={
        }
    return render(request,template,context)
