from django.db import models
import bcrypt
import re
import datetime

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
    objects=UserManager()

class Cause(models.Model):
    name = models.CharField(max_length=255)
    mission_stmt = models.TextField()
    desc = models.TextField()
    ein = models.IntegerField()
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
