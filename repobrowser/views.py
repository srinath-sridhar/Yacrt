from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required

# home page of the user on successful login
# displays all the repositories that user has access to
@login_required(login_url='/registration/signin/')
def repos_home(request):
    user_name = request.session.get('name')
    user_name = strip_tags(user_name)
    return render(request, "repobrowser/repos_home.html", {'user_name':user_name})
