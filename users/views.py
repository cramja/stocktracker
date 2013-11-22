from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.views import login as loginview

from models import Stock, UserStockMapping

def login2(request):
	if request.user.is_authenticated():
		return redirect("/users/profile/")
	else:
		return loginview(request, template_name='users/login.html')

def login(request):
<<<<<<< HEAD
# old login function.
# check out that code, oh yeah, so sophisticated
=======
>>>>>>> origin/HEAD
	if request.user.is_authenticated(): #if the user is already logged in, redirect to the profile page
		return render(request, 'users/profile.html')
		
	if(request.method == "POST"):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			auth_login(request, user)
			return redirect('/users/profile/')
		else:
			error = 'The username/password combo is incorrect'
			return render(
				request, 
				'users/login.html', 
				{ 'error' : error, 'username' : request.POST['username'], }
				)
	else:
		return render(request, 'users/login.html')

@login_required
def logout_view(request):
	logout(request)
	return render(request, 'users/logout.html')

@login_required
def profile(request):
	return render_to_response('users/profile.html', {'stocks': UserStockMapping.objects.filter(user=request.user)})


@login_required
def addStock(request):
	if (request.method =="POST"):
		stockNameToAdd = request.POST["stock"]
		matchingStock = Stock.objects.filter(name=stockNameToAdd)
		if (len(matchingStock) == 0):
			matchingStock = Stock()
			matchingStock.name = stockNameToAdd
			matchingStock.save()
			print "created stock:", matchingStock
		else:
			matchingStock = matchingStock[0]
			print "found stock:", matchingStock
		if len(UserStockMapping.objects.filter(user=request.user, stock=matchingStock)) == 0:
			mapping = UserStockMapping()
			mapping.user = request.user
			mapping.stock = matchingStock
			mapping.save()
		return redirect("/users/profile/")
	else:
		return redirect("/users/profile/")

def register(request):
	if request.user.is_authenticated():
		return redirect("/users/profile/")
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