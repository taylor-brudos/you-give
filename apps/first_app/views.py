from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'first_app/index.html')


def userProfile(request,id):
    return render(request,'first_app/userprofile.html')

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



