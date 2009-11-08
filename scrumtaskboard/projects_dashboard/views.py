from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from models import Project

@login_required
def index(request):
    projectsList = Project.objects.filter(userprojectrole__user__user__exact=request.user)
    return render_to_response('projects_dashboard/index.html',
        {'projectsList': projectsList})
