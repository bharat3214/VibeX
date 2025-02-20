from django.shortcuts import render,redirect
from .models import *
from django.db import connection
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.

def login_page(request):
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid Username")
            return redirect("/login")
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"Invalid Password")
            return redirect("/login")


        else:
            login(request,user)
            return redirect("/chat")

    return render(request,'login.html')


def home(request):
    return render(request,'home.html')

def logout_page(request):
    logout(request)
    return redirect('/login')

def register_page(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"Username already taken!")
            return redirect('/register')
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,

        )
        user.set_password(password)
        user.save()

        messages.info(request,'Account Created Successfully')
        return redirect('/register')
    
    return render(request, 'register.html')

@login_required(login_url="/login/")
def chat(request):
    return render(request,'chat.html')
