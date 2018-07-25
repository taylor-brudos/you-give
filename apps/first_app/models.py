from django.db import models
import bcrypt
import re
import datetime

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

class Donation_has_cause(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    amount = models.FloatField()
    cause = models.ForeignKey(Cause, related_name="donation_has_causes")
    donation = models.ForeignKey(Donation, related_name="donation_has_causes")
