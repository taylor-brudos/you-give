from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'first_app/index.html')

def userProfile(request,id):
    return render(request,'first_app/userprofile.html')