import django.contrib.auth.models
from django.core.management.base import django
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, unique=True)

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now=True)

class Permission(models.Model):
    name = models.CharField(max_length=200)

class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)

class UserProjectRole(models.Model):
    user = models.ForeignKey(UserProfile)
    role = models.ForeignKey(Role)
    project = models.ForeignKey(Project)

