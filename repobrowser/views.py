from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from repobrowser.models import Repository
from svnclient import svncommands

"""
 Home page of the user on successful login
 Displays all the repositories that user has access to
    """
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

"""
 Page that lists all the revisions for a given repository repository
 Http GET parms repo_url  = Absolute URL for the repository,
                repo_name = Name of the repository displayed on the page
                repo_url  = absolute url of the repository
    """    
@login_required(login_url='/registration/signin/')
def get_repo_revisions(request):
    user_name = get_user_name(request)
    repo_abs_url = request.GET['repo_url']
    repo_name = request.GET['repo_name']    
    repo_revisions = svncommands.get_revision_details(repo_abs_url)
    return render(request, "repobrowser/repo_revisions.html",
                   {'user_name':user_name, 
                    'repo_revisions':repo_revisions,
                    'repo_name' : repo_name,
                    'repo_url':repo_abs_url})

"""
 Page shows unified diff for every file path affected in this revision
 Http GET params repo_url              = absolute url of the repository
                 rev_number            = revision number of the repository
                 repo_name             = Name of the repository displayed on the page
    """
@login_required(login_url='/registration/signin/')
def get_revision_changes(request):
    user_name = get_user_name(request)
    repo_abs_url = request.GET['repo_url']
    repo_rev_number = request.GET['rev_number']
    repo_name = request.GET['repo_name']
    changes = svncommands.get_all_changed_paths(repo_abs_url, repo_rev_number)
    changed_paths = []     
          
    for path in changes:
        changed_path = {} 
        changed_path['change'] = path
        if path.get_action_on_file() is "Modified":
            changed_path['diff'] = "\n".join(svncommands.get_unified_html_diff(repo_abs_url, path.get_absolute_path(), int(repo_rev_number)))
        else:
            changed_path['diff'] = ""
        changed_paths.append(changed_path)
    for path in changed_paths:
        print path['diff']
    return render(request, "repobrowser/repo_revision_changes.html",
                {'user_name':user_name,
                'repo_name':repo_name,
                'rev_number':repo_rev_number,
                'changed_paths':changed_paths})
