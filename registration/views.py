from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login

#Displays the login form 
def signin_form(request):
    return render_to_response('registration/signin_form.html',context_instance=RequestContext(request));

def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse("User authenticated")
        else:
            return HttpResponse("User account disabled")
    else:
        return HttpResponse("User invalid")
