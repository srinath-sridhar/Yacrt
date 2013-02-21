from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

#Displays the login form 
def signin_form(request):
    return render_to_response('registration/signin_form.html',context_instance=RequestContext(request));

def authenticate_user(request):
    return HttpResponse("User Authenticated")   

