from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import  ContentType
from django.http import HttpResponseRedirect, HttpResponse
from repobrowser.models import Repository
from svnclient import svncommands
from svnclient import exceptions


INVALID_FILES = {
    '.settings', '.classpath', '.idea', '.DStore'
}


def construct_abs_path(repo_path, relative_path):
    i = 2
    j = len(repo_path) - 2
    while j > -1:
        if relative_path[:i] == repo_path[j:]:
            return repo_path[:j] + relative_path
        j -=1
        i +=1
    return repo_path + relative_path[1:]

"""
 Home page of the user on successful login
 Displays all the repositories that user has access to
    """
@login_required(login_url='/registration/signin/')
def repos_home(request):
    user_name = get_user_name(request)
    repos = get_repos(request.user)
    messages = __get_messages(request)
    return render(request, "repobrowser/repos_home.html", {'username':user_name, 'repos':repos, 'messages': messages})

# will retrieve all messages related to any previous actions and clear the session variable
def __get_messages(request):
    returnList = request.session['messages']
    request.session['messages'] = {}
    return returnList

# retireves all repos the user has access to
def get_repos(user):
    repos = Repository.objects.filter(repo_access_group__in=user.groups.all()) 
    return repos

# gets user name form session variable and escapes html tags
def get_user_name(request):
    user_name = request.session.get('username')
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
    try:
        repo_revisions = svncommands.get_revision_details(repo_abs_url)
        repo_id = request.GET['repo_id']
        return render(request, "repobrowser/repo_revisions.html",
                       {'user_name':user_name,
                        'repo_revisions':repo_revisions,
                        'repo_name' : repo_name,
                        'repo_url':repo_abs_url,
                        'repo_id':repo_id})
    except exceptions.SVNExceptions, e:
        request.session['messages'] = {
            'error' : e.value
        }
        return redirect("/repos/home/")

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
    repo_id = request.GET['repo_id']
    changes = svncommands.get_all_changed_paths(repo_abs_url, repo_rev_number)
    changed_paths = []

    for path in changes:
        changed_path = {}
        changed_path['change'] = path
        common_path = construct_abs_path(repo_abs_url, path.get_relative_path())
        changed_path['diff'] = svncommands.get_unified_html_diff(repo_abs_url, common_path,int(repo_rev_number))
        changed_paths.append(changed_path)

    return render(request, "repobrowser/repo_revision_changes.html",
                {'user_name':user_name,
                'repo_name':repo_name,
                'rev_number':repo_rev_number,
                'changed_paths':changed_paths,
                'repo_id':repo_id})

def save(request):
    print "Called save!"
    user = User.objects.get(username=request.session['username'])
    print user.username
    group = Group.objects.filter(user__username__exact=request.session['username'], name__exact=(request.session['username']+"'s group"))
    if len(group) == 0:
        print "setting errors"
        request.session['messages'] = {
            'error' : "Oops! You can't add a repository as this time since you are a user from the previous release. Please contact Admin to adapt you to this version."
        }
    else:
        print "Creating objects"
        new_repo = Repository.objects.create(repo_access_group_id=group[0].pk, repo_created_by=user)
        new_repo.repo_name = request.POST['repo_name']
        new_repo.repo_description = request.POST['repo_descrip']
        new_repo.repo_url = request.POST['repo_url']
        # Create Group Permissions
        repository_content_type = ContentType.objects.get(app_label='repobrowser', model='Repository')
        delete_permission = Permission.objects.get(codename='delete_repository',
                                       name='Can delete repository',
                                       content_type=repository_content_type)
        change_permission = Permission.objects.get(codename='change_repository',
                                                      name='Can change repository',
                                                      content_type=repository_content_type)
        user.user_permissions.add(change_permission, delete_permission)
        user.save()
        new_repo.save()
        request.session['messages']  = {
            'success' : "Repository has been successfully added."
        }
    return redirect('/repos/home/')



def __isAValidFile(relative_file_path):
    splitFilePath = relative_file_path.rsplit('/', 1)
    if len(splitFilePath) > 1:
        typeSplit = splitFilePath[1].split('.')
        if len(typeSplit) > 1:
            if typeSplit[0] == '':
                return False
            else:
                return True
    return False

