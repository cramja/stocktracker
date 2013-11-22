from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as authlogin


def login(request):
	if request.user.is_authenticated(): #if the user is already logged in, redirect to the profile page
		return HttpResponseRedirect('/users/profile/')
		
	if(request.method == "POST"):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			authlogin(request, user)
			return HttpResponseRedirect('/users/profile', request)
		else:
			return HttpResponse('The username/password combo is incorrect')
	else:
		context = RequestContext(request)
		return render_to_response('users/login.html', context)

def logout_view(request):
	logout(request)
	return render(request, 'users/logout.html')

@login_required
def profile(request):
	return render(request, 'users/profile.html')

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(redirect_to='/users/logout/')
	if 'errors' in request.session: #user previously tried to enter stuff in this form
		error = request.session['errors']
		enteredusername = ""
		if 'enteredusername' in request.session:
			enteredusername = request.session['enteredusername']
		context = RequestContext(request, {'errors' : error, 'enteredusername' : enteredusername})
		return render_to_response('users/register.html', context)

	context = RequestContext(request)
	return render_to_response('users/register.html', context)

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
			string = 'Cool, we have created this account, ' + newuser.username
			return HttpResponse(string)
		enteredusername = request.POST['username']
		request.session['errors'] = error
		request.session['enteredusername'] = enteredusername
		context = RequestContext(request)
		context['errors']= error
		return redirect('/users/register/', context)
	else:
		return HttpResponseRedirect(redirect_to='/users/register/')