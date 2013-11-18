from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect

def index(response):
	return render(response, 'index.html')

def testvisuals(response):
	return render(response, 'testvisuals.html')

def testsessions(request):
	if request.method=='POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			# Correct password, and the user is marked "active"
			auth.login(request, user)
			# Redirect to a success page.
			assert False
			return HttpResponseRedirect("/account/loggedin/")
		else:
			# Show an error page
			return HttpResponseRedirect("/account/invalid/")
	else:
		return render(request, 'testsessions.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/") #redirects user to homepage
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", 
    	{
        	'form': form,
    	})
    
def visuals(response):
	return render(response, 'visuals.html')
