from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

#Displays the login form 
def signin_form(request):
    return render_to_response('registration/signin_form.html', context_instance=RequestContext(request));

#Does the actual user authentication
def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['username'] = username
            request.session['messages']= {}
            print user.has_perm('auth.change_group')
            return redirect('/repos/home/')
        else:
            return render(request, 'registration/signin_form.html', {'error_message': "User account disabled",})
    else:
        return render(request, 'registration/signin_form.html', {'error_message': "User invalid"})

# Log out function. Uses django auth model to clear session
def signout(request):
    if request.user is None:
        return render(request, 'registration/signin_form.html', {'success_message': "User successfully logged out",})
    else:
        logout(request)
        return render(request, 'registration/signin_form.html', {'success_message': "User successfully logged out",})

def create_new(request):
    print "Create called"
    return render(request, 'registration/new.html')

# Creation of new user implies creation of a default group for that user.
def save_user(request):
    print "Save called" + request.POST['user_name']
    new_user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
    new_user.username = request.POST['user_name']
    group_name = new_user.username + "'s group"
    group = Group.objects.create(name=group_name)
    group.save()
    new_user.groups.add(group)
    content_type = ContentType.objects.get(app_label='auth', model='Group')
    permission = Permission.objects.get(codename='change_group',
                                           name='Can change group',
                                           content_type=content_type)
    new_user.user_permissions.add(permission)
    new_user.save()
    return HttpResponseRedirect('/')