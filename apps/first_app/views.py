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
    
def displayStatement(request):
    return render(request, 'first_app/statement.html')

def adminUsers(request):
    return render(request, 'first_app/admin_users.html')

def adminCauses(request):
    return render(request, 'first_app/admin_causes.html')
