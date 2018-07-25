from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt

from .models import *


# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return redirect('/explore')
    else:
        return render(request,'first_app/index.html')

def userProfile(request):
    if 'user_id' in request.session:
        context = {
            "user":User.objects.get(id=request.session['user_id']),
            "all_users":User.objects.all()
        }
        return render(request,'first_app/userprofile.html',context)

def explore(request):
    return render(request, 'first_app/explore.html')

def displayCharity(request):
    return render(request, 'first_app/charity.html')

def addGroup(request):
    return render(request, 'first_app/newgroup.html')

def checkout(request):
    return render(request, 'first_app/checkout.html')

def register(request):
    return render(request, 'first_app/register.html')
    
def displayStatement(request):
    return render(request, 'first_app/statement.html')

def adminUsers(request):
    return render(request, 'first_app/admin_users.html')

def adminCauses(request):
    return render(request, 'first_app/admin_causes.html')

def login(request):
    if request.method == "POST":
        errors=User.objects.login_validator(request.POST)
        if len(errors):
            request.session['loginemail']=request.POST['email']
            for key,value in errors.items():
                messages.error(request,value,extra_tags='login')
        else:
            user=User.objects.get(email=request.POST['email'])
            request.session['user_id']=user.id
            request.session['user_level']=user.user_level
            request.session['first_name']=user.first_name
            messages.success(request,"Successfully logged in!")
        return redirect('/')
      
def registerUser(request):
    if request.method=='POST':
        password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        registerUser=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password_hash, user_level=0)
    return redirect('/explore')

def logout(request):
    request.session.clear()
    return redirect('/')