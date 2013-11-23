from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.contrib.auth.views import login as loginview

from stocks.models import Stock, UserStockMapping

def index(request):
	return render(request, 'stocks/base.html')
	
def quotes(request):
	return render(request, 'stockview/quotes.html')

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
	auth_logout(request)
	return redirect("/")

def register(request):
	if request.user.is_authenticated():
		return redirect("/")
	return render(request, 'users/register.html')

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
			return redirect("/")
	return redirect("/register/")

@login_required
def addStock(request):
	if (request.method =="POST"):
		stockNameToAdd = request.POST["stock"].upper()
		matchingStock = Stock.objects.filter(name=stockNameToAdd)
		if (len(matchingStock) == 0):
			matchingStock = Stock()
			matchingStock.name = stockNameToAdd
			matchingStock.save()
		else:
			matchingStock = matchingStock[0]
		if len(UserStockMapping.objects.filter(user=request.user, stock=matchingStock)) == 0:
			mapping = UserStockMapping()
			mapping.user = request.user
			mapping.stock = matchingStock
			mapping.save()
	return redirect("/")

@login_required
def removeStock(request):
	if (request.method =="POST"):
		stockNameToRemove = request.POST["stock"]
		stock = Stock.objects.get(name=stockNameToRemove)
		mapping = UserStockMapping.objects.get(user=request.user, stock=stock)
		mapping.delete()
		mappingsToStock = UserStockMapping.objects.filter(stock=stock)
		# If there are no more references to the stock, it can be deleted
		if (len(mappingsToStock) == 0):
			stock.delete()
	return redirect("")