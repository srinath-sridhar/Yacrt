from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group, User
from repobrowser.models import Repository
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from datetime import datetime
from commentmgr.models import Comment
import sys

"""
    checks if user has access to repo_id
    params:
            user_id - id(primary key) of user
            repo_id - id(primary key) of the repository
    returns:
            true - if user has access to repository
            false - other wise
"""
def can_user_access_repo(user_id, repo_id):
    try:
        repo = Repository.objects.get(id=repo_id)
        if repo is None:
            print "invalid repo"
        else:
            try:
                user = User.objects.get(pk=user_id)
                access_group_id = repo.repo_access_group.id
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

"""
    checks if user can change / delete a comment
    params:
            user_id    - id(primary key) of user
            comment_id - id(primary key) of the comment
    returns:
            comment object  - if user can change / delete comment
            None - other wise
"""
def can_user_change_comment(user_id, comment_id):
    try:
        comment = Comment.objects.filter(id=comment_id, user=user_id)
        if comment is None or len(comment) == 0:
            return None
        else:
            return comment[0]
    except:
        return None

"""
    creates and saves a comment object in the datebase
    params:
            user_id - user who created the comment
            repository_id - on which repository
            revision_number - for which revision number in repository
            path - path of particular file in the given revision of the repository
            line - line number this comment applies to
            content - content of the comment
    returns:
            comment_id, timestamp - on successfully saving object to datebase
            None - if there is an error
"""
def create_new_comment(user_id, repository_id, revision_number, path, line, comment):
    try:
        now = datetime.now()
        comment = Comment.objects.create(
                        user_id=user_id,
                        repo_id=repository_id,
                        repo_revision=revision_number,
                        file_path=path,
                        line_number=line,
                        content=comment,
                        timestamp=now)
        return (comment.id, now)
    except:
        print sys.exc_info()
        return (None, None)

"""
    updates the comment content and timestamp
    params:
            comment - object corresponding to comment in database
            new_content - updated content for the comment
    returns:
            0 - on success
            1 - on error
"""
def update_comment(comment, new_content):
    try:
        now = datetime.now()
        comment.timestamp = now
        comment.content = new_content
        comment.save()
        return now
    except:
        return None

"""
    deletes the comment object from the database
    params:
            comment - object corresponding to comment in database
    returns:
            0 - on success
            1 - otherwise
"""
def destroy_comment(comment):
    try:
        comment.delete()
        return 0
    except:
        return 1

"""
    gets all comments from database
    params:
        repo_id - id of the repository
        revision_number - particular revision of the given repository
        file_path - file within the repository
"""
def get_all_comments(repository_id, revision_number, file):
    try:
        comments = Comments.objects.filter(
                                repo_id = repository_id,
                                repo_revision = revision_number,
                                file_path = file)
        return comments
    except:
        return None

"""
    Create a new comment and saves it in the database
    params from HTTP request:
            repo_id = id of the repository
            revision_number = repo revision number
            file_path = path to the file
            line number = line_number in file
            content = comment content
            user_id  = from session

    Prerequisites:
            User should be logged in.
            User should have access to the repository.
"""
@login_required(login_url='/registration/signin/')
def create(request):
    data = {}
    user_id = request.session['user_id']
    repo_id = request.GET['repo_id']

    #check if user has access to repo
    if can_user_access_repo(user_id, repo_id) is True:
        #Get params from get request
        revision_number = request.GET['revision_number']
        file_path = request.GET['file_path']
        line_number = request.GET['line_number']
        content = request.GET['content']

        #create comment
        (comment_id, ts) = create_new_comment(user_id, repo_id, revision_number, file_path, line_number, content)
        if comment_id != None:
            author = request.session['username']
            data['error_code'] = 0
            data['error_msg'] = "Comment created successfully"
            data['author'] = author
            data['timestamp'] = str(ts)
            data['comment_id'] = comment_id
        else:
            data['error_code'] = 2
            data['error_msg'] = "Oops something went wrong! unable to create comment, try again"
            data['author'] = ""
            data['timestamp'] = ""
            data['comment_id'] = ""
    else:
        data['error_code'] = 1
        data['error_msg'] = "User does not have accesss to the repository"
        data['author'] = ""
        data['timestamp'] = ""
        data['comment_id'] = ""

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

"""
    Update the content of an existing comment
    params from HTTP request:
            comment_id = id of the comment
            user_id  = from session

    Prerequisites:
            User should be logged in.
            User should have access to the repository.
            User is allowed to change comment
"""
@login_required(login_url='/registration/signin/')
def edit(request):
    data = {}
    user_id = request.session['user_id']
    comment_id = request.GET['comment_id']
    repo_id = request.GET['repo_id']

    #check if user has access to repo
    if can_user_access_repo(user_id, repo_id) is True:
        comment = can_user_change_comment(user_id, comment_id)
        if comment != None:
            new_content = request.GET['new_content']
            new_timestamp = update_comment(comment, new_content)
            if new_timestamp != None:
                data['error_code'] = 0
                data['error_msg'] = "Comment updated successfully"
                data['new_timestamp'] = new_timestamp

            else:
                data['error_code'] = 2
                data['error_msg'] = "Oops something went wrong! unable to update comment, try again"
                data['new_timestamp'] = ""
        else:
            data['error_code'] = 3
            data['error_msg'] = "User is not allowed to change comment"
            data['new_timestamp'] = ""

    else:
        data['error_code'] = 1
        data['error_msg'] = "User does not have accesss to the repository"
        data['new_timestamp'] = ""

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

"""
    delete an existing comment
    params from HTTP request:
            comment_id = id of the comment
            user_id  = from session

    Prerequisites:
            User should be logged in.
            User should have access to the repository.
            User is allowed to change comment
"""
@login_required(login_url='/registration/signin/')
def destroy(request):
    data = {}
    user_id = request.session['user_id']
    comment_id = request.GET['comment_id']
    repo_id = request.GET['repo_id']

    #check if user has access to repo
    if can_user_access_repo(user_id, repo_id) is True:
        comment = can_user_change_comment(user_id, comment_id)
        if comment != None:
            if destroy_comment(comment) == 0:
                data['error_code'] = 0
                data['error_msg'] = "Comment deleted successfully"

            else:
                data['error_code'] = 2
                data['error_msg'] = "Oops something went wrong! unable to delete comment, try again"

        else:
            data['error_code'] = 3
            data['error_msg'] = "User is not allowed to delete comment"

    else:
        data['error_code'] = 1
        data['error_msg'] = "User does not have accesss to the repository"

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

"""
    get all the comments for a given version of a
    particular file in a repository

    params for HTTP request
            repo_id = id of the repository
            revision_number = repo revision number
            file_path = path to the file
            user_id  = from session
"""
@login_required(login_url='registration/signin/')
def all(request):
    data = {}
    user_id = request.session['user_id']
    repo_id = request.GET['repo_id']
    #check if user has access to repo
    if can_user_access_repo(user_id, repo_id) is True:
        file_path = request.GET['file_path']
        revision_number = request.GET['revision_number']
        comments = get_all_comments(repo_id, revision_number, file_path)
        if comments != None:
            data['error_code'] = 0
            data['error_msg'] = "Comments retrieved successfully"
            data['comments'] = comments
        else:
            data['error_code'] = 2
            data['error_msg'] = "Oops something went wrong! unable to retrieve comments, try again"

    else:
        data['error_code'] = 1
        data['error_msg'] = "User does not have accesss to the repository"
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')