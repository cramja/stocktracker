from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.contrib.auth.views import login as loginview
from django.core.exceptions import ObjectDoesNotExist

from stocks.models import Stock, UserProfile

def index(request):
	if request.user.is_authenticated():
		profile = request.user.profile
		stocks_codes = profile.interests.all()
		all_stocks = list()
		for stock in Stock.objects.all():
			if stock not in stocks_codes:
				all_stocks.append(stock)
		return render(request, 'base.html', {'stocks': stocks_codes, 'stocks_codes': all_stocks})
	else:
		return render(request, 'base.html', {'stocks_codes': Stock.objects.all()})

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

def getStocks(request):
    """
    Gets all of the stocks from the database and converts them
    to JSON with the associated metadata
    """
    stocks = Stock.objects.all()
    if not messages.exists:
        return HttpResponse("{}")

    if request.method == "GET":
        retList = list()
        for s in stocks:
            retList.append({
                "code": s.code,
                "name": s.name
            })

        return HttpResponse(json.dumps(retList))

@login_required
def addStock(request):
	if (request.method == 'POST'):
		stockID = request.POST['stock'].upper()
		matchingStock = Stock.objects.get(code=stockID)
		profile, created = UserProfile.objects.get_or_create(user=request.user)
		profile.interests.add(matchingStock)
	return redirect("/")

@login_required
def removeStock(request):
	if (request.method == 'POST'):
		print request.POST
		stockID = request.POST['stock'].upper()
		matchingStock = Stock.objects.get(code=stockID)
		profile = UserProfile.objects.get(user=request.user)
		profile.interests.remove(matchingStock)
	return redirect("/")
