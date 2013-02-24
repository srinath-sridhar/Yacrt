from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from repobrowser.models import Repository


# home page of the user on successful login
# displays all the repositories that user has access to
@login_required(login_url='/registration/signin/')
def repos_home(request):
    user_name = request.session.get('name')
    user_name = strip_tags(user_name)
    repos = get_repos(request.user)
    return render(request, "repobrowser/repos_home.html", {'user_name':user_name, 'repos':repos})

# retireves all repos the user has access to
def get_repos(user):
    repos = Repository.objects.filter(repo_access_group__in=user.groups.all()) 
    return repos
    
