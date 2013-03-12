# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from repobrowser.models import Repository
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

def can_user_access_repo(user_id, repo_id):
    try:
        repo = Repository.objects.get(id=repo_id)
        if repo is None:
            print "invalid repo"
        else:
            try:
                user = User.objects.get(pk=user_id)
                access_group_id = repo.repo_access_group.id
                print access_group_id
                group = user.groups.filter(id=access_group_id)
                if len(group) == 0:
                    print "user not allowed"
                    return False
                else:
                    print "user allowed"
                    return True
            except:
                print "error retriving user / group data"
                return False
    except:
        print "rerror retriving repo data"
        return False

def create_new_comment(user_id, repo_id, revision_number, file_path, ):

@login_required(login_url='/registration/signin/')
def create(request):
    repo_id = request.GET['repo_id']
    user_id = request.session['user_id']

    can_user_access_repo(user_id, repo_id)

    data = simplejson.dumps({})
    return HttpResponse(data, mimetype='application/json')

def save(request):
    data = simplejson.dumps({})
    return HttpResponse(data, mimetype='application/json')

def edit(request):
    data = simplejson.dumps({})
    return HttpResponse(data, mimetype='application/json')

def destror(request):
    data = simplejson.dumps({})
    return HttpResponse(data, mimetype='application/json')

