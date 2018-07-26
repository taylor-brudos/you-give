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

def userProfile(request,id):
    return render(request,'first_app/userprofile.html')

def explore(request):
    causes = Cause.objects.all()
    context = {
        'causes': causes
    }
    return render(request, 'first_app/explore.html', context)

def displayCharity(request, cause_id):
    cause = Cause.objects.get(id=cause_id)
    context = {
        'cause': cause
    }
    return render(request, 'first_app/charity.html', context)

def addGroup(request):
    return render(request, 'first_app/newgroup.html')

def checkout(request):
    return render(request, 'first_app/checkout.html')

def register(request):
    return render(request, 'first_app/register.html')
    
def displayStatement(request):
    return render(request, 'first_app/statement.html')

def adminUsers(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'first_app/admin_users.html', context)

def adminCauses(request):
    causes = Cause.objects.all()
    context = {
        'causes': causes
    }
    return render(request, 'first_app/admin_causes.html', context)

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

def deleteUser(request):
    if request.method=='POST':
        this_user = User.objects.get(id=request.POST['user_id'])
        this_user.delete()
    return redirect('/admin/users')

def updateUser(request):
    if request.method=='POST':
        this_user = User.objects.get(id=request.POST['user_id'])
        this_user.first_name = request.POST['first_name']
        this_user.last_name = request.POST['last_name']
        this_user.email = request.POST['email']
        this_user.user_level = request.POST['user_level']
        this_user.save()
        return redirect('/admin/users')

def addUser(request):
    if request.method=='POST':
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash, user_level=request.POST['user_level'])
    return redirect('/admin/users')

def deleteCause(request):
    if request.method == 'POST':
        this_cause = Cause.objects.get(id=request.POST['cause_id'])
        this_cause.delete()
    return redirect('/admin/causes')

def updateCause(request):
    if request.method == 'POST':
        this_cause = Cause.objects.get(id=request.POST['cause_id'])
        this_cause.name = request.POST['name']
        this_cause.ein = request.POST['ein']
        this_cause.mission_stmt = request.POST['mission']
        this_cause.desc = request.POST['desc']
        this_cause.revenue_id = request.POST['revenue_id']
        this_cause.save()
        return redirect('/admin/causes')

def addCause(request):
    if request.method=='POST':
        new_cause = Cause.objects.create(name=request.POST['name'], mission_stmt=request.POST['mission'], desc=request.POST['desc'], ein=request.POST['ein'],revenue=Revenue.objects.get(id=request.POST['revenue_id']), admin=User.objects.get(id=request.session['user_id']))
    return redirect('/admin/causes')