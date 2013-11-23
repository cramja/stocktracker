from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.views import login as loginview

def stocks(request):
	return render(request, "stocks/stocks.html")

def login(request):
	if not request.user.is_authenticated() and request.method == "POST": 
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			auth_login(request, user)
	#commented out error checking for now
	# 	else:
	# 		error = 'The username/password combo is incorrect'
	# 		return render(
	# 			request, 
	# 			'users/login.html', 
	# 			{ 'error' : error, 'username' : request.POST['username'], }
	# 			)
	# else:
	# 	return render(request, 'users/login.html')
	return redirect("/")

def logout(request):
	logout(request)
	return redirect("/")

def create(request):
	return redirect("/")

def register(request):
	if request.user.is_authenticated():
		return redirect("/")
	return render('users/register.html')

def create(request):
	if request.method == "POST":
		error = []
		if User.objects.filter(username__iexact=request.POST['username']).count() != 0:
			error.append("Username already taken")
		if request.POST['password1'] != request.POST['password0']:
			error.append("Passwords do not match")
		if len(error) == 0:
			newuser = User(username = request.POST['username'])
			newuser.set_password(request.POST['password0'])
			newuser.save()
			string = 'We have created an account for: ' + newuser.username
			return render("/")
	return redirect("/register/")