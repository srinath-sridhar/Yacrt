from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from repobrowser.models import Repository
from svnclient.pysclient import Pysclient


# home page of the user on successful login
# displays all the repositories that user has access to
@login_required(login_url='/registration/signin/')
def repos_home(request):
    user_name = get_user_name(request)
    repos = get_repos(request.user)
    return render(request, "repobrowser/repos_home.html", {'user_name':user_name, 'repos':repos})

# retireves all repos the user has access to
def get_repos(user):
    repos = Repository.objects.filter(repo_access_group__in=user.groups.all()) 
    return repos

# gets user name form session variable and escapes html tags
def get_user_name(request):
    user_name = request.session.get('name')
    user_name = strip_tags(user_name)
    return user_name

# Page that lists all the files present in the repository    
@login_required(login_url='/registration/signin/')
def get_repo_revisions(request):
    user_name = get_user_name(request)
    repo_abs_url = request.GET['repo_url']
    repo_name = request.GET['repo_name']
    client = Pysclient(repo_abs_url)
    repo_revisions = client.get_revisions()
    return render(request, "repobrowser/repo_revisions.html",
                   {'user_name':user_name, 
                    'repo_revisions':repo_revisions,
                    'repo_name' : repo_name})
