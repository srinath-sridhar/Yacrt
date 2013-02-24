from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
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
            request.session['name'] = user.get_full_name()
            return redirect('/registration/home/')
        else:
            return render(request, 'registration/signin_form.html', {'error_message': "User account disabled",})
    else:
        return render(request, 'registration/signin_form.html', {'error_message': "User invalid"})


@login_required(login_url='/registration/signin/')
def login_success(request):
    print request.session.get('name')
    name = request.session.get('name')
    name = strip_tags(name)
    return HttpResponse("Welcome " + name)



