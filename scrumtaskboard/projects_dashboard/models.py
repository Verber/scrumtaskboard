import django.contrib.auth.models
from django.core.management.base import django
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, unique=True)

    def __unicode__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)

    def __unicode__(self):
        return self.name

class UserProjectRole(models.Model):
    user = models.ForeignKey(UserProfile)
    role = models.ForeignKey(Role)
    project = models.ForeignKey(Project)

    class Meta:
        unique_together = (('user', 'role', 'project'))

    def __unicode__(self):
        from string import Template
        t = Template('User $user as $role on $project')
        return t.substitute(user=self.user, role=self.role, project=self.project)