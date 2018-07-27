from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum
import bcrypt
import datetime

from .models import *


# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return redirect('/explore')
    else:
        return render(request,'first_app/index.html')

def userProfile(request):
    if 'user_id' in request.session:
        user=User.objects.get(id=request.session['user_id'])
        context = {
            "user":user,
            "all_users":User.objects.all(),
            "all_causes":Cause.objects.all(),
            "user_donation":user.donations.aggregate(Sum('amount'))
        }
        return render(request,'first_app/userprofile.html',context)
    else:
        return redirect('/')

def inviteUser(request,id):
    if request.method=='POST':
        if 'user_id' in request.session:
            group=Group.objects.get(id=id)
            invitee=User.objects.get(id=request.POST['invite'])
            newInvite=Invitation.objects.create(is_accepted=False, invitee=invitee, group=group)
            return redirect('/dashboard')
        else:
            return render('/')

def acceptInvite(request,id):
    if 'user_id' in request.session:
        invitation=Invitation.objects.get(id=id)
        invitation.is_accepted=True
        invitation.save()
        return redirect('/dashboard')
    else:
        return redirect('/')

def declineInvite(request,id):
    if 'user_id' in request.session:
        invitation=Invitation.objects.get(id=id)
        invitation.delete()
        return redirect('/dashboard')
    else:
        return redirect('/')


def explore(request):
    if 'cart' not in request.session:
        request.session['cart'] = [{'total': 0.00}]
    causes = Cause.objects.all()
    context = {
        'causes': causes
    }
    return render(request, 'first_app/explore.html', context)

def displayCharity(request, cause_id):
    cause = Cause.objects.get(id=cause_id)
    context = {
        'cause': cause,
        'causes': Cause.objects.all()[:5]
    }
    return render(request, 'first_app/charity.html', context)

def displayCharity_give(request, cause_id):
    if request.method == 'POST':
        x = request.session['cart']
        x[0]['total'] += float(request.POST['amount'])
        if request.POST['source'] == 'group':
            x.append({'cause_id': cause_id, 'cause_name':Cause.objects.get(id=cause_id).name, 'amount': request.POST['amount'], 'source': request.POST['source'],'group': request.POST['group_id']})
        else:
            x.append({'cause_id': cause_id, 'cause_name':Cause.objects.get(id=cause_id).name, 'amount': request.POST['amount'], 'source': request.POST['source']})
        messages.success(request,"This donation has been added to your cart!",extra_tags="cart")
        request.session['cart'] = x
        print(request.session['cart'])
    return redirect('/charity/'+cause_id)

def addToWishList(request,id):
    if 'user_id' in request.session:
        wisher = User.objects.get(id=request.session['user_id'])
        cause = Cause.objects.get(id=id)
        wishList=cause.wishers.add(wisher)
        messages.success(request,"This Cause has been added to your wishlist!",extra_tags="wishlist")
        return redirect('/charity/'+id)
    else:
        return redirect('/')

# def addToCart(request,id):
#     if 'user_id' in request.session:
#         if request.method=='POST':
#             print("before:",request.session['cart'])
#             cart=request.session['cart']
#             cart.append({"cause":Cause.objects.get(id=id),"amount":request.POST['amount'],"source":request.POST['source']})
#             cart[0]['total']+=request.POST['amount']
#             request.session['cart'] = cart
#             print("after:",request.session['cart'])
#         return redirect('/dashboard')
#     else:
#         return redirect('/')

def addGroup(request):
    if 'user_id' in request.session:
        context={
            "all_causes":Cause.objects.all()
        }
        return render(request, 'first_app/newgroup.html',context)

def createGroup(request):
    if 'user_id' in request.session:
        createGroup=Group.objects.create(title=request.POST['title'], goal=request.POST['goal'],contributions=0, target_date=request.POST['target_date'],organizer=User.objects.get(id=request.session['user_id']),cause=Cause.objects.get(id=request.POST['org']))
        invitation=Invitation.objects.create(is_accepted=True, invitee=User.objects.get(id=request.session['user_id']),group=Group.objects.get(id=createGroup.id))
    return redirect('/dashboard')

def updateGroup(request,id):
    if request.method=='POST':
        if 'user_id' in request.session:
            group=Group.objects.get(id=id)
            group.goal=request.POST['goal']
            group.cause=Cause.objects.get(id=request.POST['org'])
            if len(request.POST['target_date'])>1:
                group.target_date=request.POST['target_date']
            group.save()
            return redirect('/dashboard')
        else:
            return redirect('/')


def checkout(request):
    return render(request, 'first_app/checkout.html')

def processCheckout(request):
    if "user_id" in request.session:
        for donation in range(1,len(request.session['cart'])):
            cause=Cause.objects.get(id=request.session['cart'][donation]['cause_id'])
            amount=request.session['cart'][donation]['amount']
            giver=User.objects.get(id=request.session['user_id'])
            donated = Donation.objects.create(giver=giver,amount=amount,cause=cause)
            if request.session['cart'][donation]['source'] == 'group':
                group=Group.objects.get(id=request.session['cart'][donation]['group'])
                group.contributions+=float(amount)
                group.save()
                donated.groups.add(group)
                print("Source group: ",donated.__dict__)
            if request.session['cart'][donation]['source'] == 'wishlist':
                removeWishlist=User.objects.get(id=request.session['user_id']).wished_causes.remove(cause)
        del request.session['cart']
        return redirect('/thankyou')
    else:
        return redirect('/')

def register(request):
    return render(request, 'first_app/register.html')
    
def displayStatement(request):
    user=User.objects.get(id=request.session['user_id'])
    context = {
        'now': datetime.datetime.now(),
        'user': user,
        'user_donation':user.donations.aggregate(Sum('amount'))
    }
    return render(request, 'first_app/statement.html', context)

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
        request.session['user_id']=registerUser.id
        request.session['first_name']=registerUser.first_name
        request.session['user_level']=registerUser.user_level
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

def thankyou(request):
    if 'user_id' in request.session:
        if 'cart' not in request.session:
            request.session['cart'] = [{'total': 0.00}]
        return render(request,'first_app/thankyou.html')
    else:
        return redirect('/')