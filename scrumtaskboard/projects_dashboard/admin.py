from scrumtaskboard.projects_dashboard.models import *
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserProjectRole)



