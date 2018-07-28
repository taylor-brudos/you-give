from django.db import models
import bcrypt
import re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login_validator(self,postData):
        errors={}
        user=User.objects.filter(email=postData['email'])
        if len(postData['email'])<1 or len(postData['password'])<1:
            errors['emptyField']="Email and password fields cannot be empty"
        elif not len(user):
            errors['noemail']="Invalid login!"
        elif not bcrypt.checkpw(postData['password'].encode(), user.values()[0]['password'].encode()):
            errors['failedAuth']="Invalid login!"
        return errors
    def registration_validator(self,postData):
        errors={}
        user = User.objects.filter(email=postData['email'])
        if len(user) > 0:
            errors['duplicate'] = 'Email already taken'
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters'
        elif str.isalpha(postData['first_name']) == False:
            errors['first_name'] = 'First name must only be letters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters'
        elif str.isalpha(postData['last_name']) == False:
            errors['last_name'] = 'Last name must only be letters'
        if len(postData['email']) < 1:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not valid'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        elif postData['password'] != postData['confirm_password']:
            errors['confirm_pw'] = 'Passwords must match'
        return errors

class Revenue(models.Model):
    revenue = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    profile_pic = models.TextField()
    objects=UserManager()

class Cause(models.Model):
    name = models.CharField(max_length=255)
    mission_stmt = models.TextField()
    desc = models.TextField()
    ein = models.IntegerField()
    logo_img=models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    admin = models.ForeignKey(User, related_name="causes")
    revenue = models.ForeignKey(Revenue, related_name="causes")
    wishers = models.ManyToManyField(User, related_name="wished_causes")

class Group(models.Model):
    title = models.CharField(max_length=255)
    goal = models.FloatField()
    contributions = models.FloatField()
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    organizer = models.ForeignKey(User, related_name="groups")
    cause = models.ForeignKey(Cause, related_name="groups")

class Invitation(models.Model):
    is_accepted = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    invitee = models.ForeignKey(User, related_name="invitations")
    group = models.ForeignKey(Group, related_name="invitations")

class Donation(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    giver = models.ForeignKey(User, related_name="donations")
    groups = models.ManyToManyField(Group,related_name="donations")
    amount = models.FloatField()
    cause = models.ForeignKey(Cause, related_name="donation_has_causes")

# class Donation_has_cause(models.Model):
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     amount = models.FloatField()
#     cause = models.ForeignKey(Cause, related_name="donation_has_causes")
#     donation = models.ForeignKey(Donation, related_name="donation_has_causes")
