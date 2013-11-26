from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login

import random, datetime
from urllib.request import urlopen
from urllib.error import *

from stocks.models import Stock

def index(request):
	if request.user.is_authenticated():
		profile = request.user.profile
		userStocks = profile.interests.all()
		# any stock that is not in userStocks
		otherStocks = Stock.objects.exclude(pk__in=userStocks.values_list('pk', flat=True))
		if (len(userStocks) == 0):
			userStocks = None
		recommendedStocks = otherStocks.filter(recommended=True)
		if (len(recommendedStocks) == 0):
			recommendedStocks = None
		return render(request, 'profile.html', {'user_stocks': userStocks, 'other_stocks': otherStocks, 'recommended': recommendedStocks})
	else:
		return render(request, 'profile.html', {'stocks_codes': Stock.objects.all(), 'recommended': None})

def login(request):
	if not request.user.is_authenticated() and request.method == "POST":
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			auth_login(request, user)
	return redirect("/")

def logout(request):
	auth_logout(request)
	return redirect("/")

def register(request):
	if request.user.is_authenticated():
		return redirect("/")
	return render(request, 'register.html')

def create(request):
	if request.method == "POST":
		if User.objects.filter(username__iexact=request.POST['username']).count() != 0:
			# Username is already in use
			return redirect("/register")
		if request.POST['password1'] != request.POST['password0']:
			# Passwords don't match
			return redirect("/register")
		newUser = User(username = request.POST['username'])
		newUser.set_password(request.POST['password0'])
		newUser.save()
	return redirect("/")

def getStocks(request):
	# Gets all of the stocks from the database and converts them
	# to JSON with the associated metadata
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
		stockCode = request.POST['stock'].upper()
		stock = Stock.objects.get(code=stockCode)
		profile = request.user.profile
		profile.interests.add(stock)
		profile.save()
	return redirect("/")

@login_required
def removeStock(request):
	if (request.method == 'POST'):
		checkboxes = request.POST.getlist('stock')
		userStocks = request.user.profile.interests
		for stock in checkboxes:
			stock = Stock.objects.get(code=stock)
			userStocks.remove(stock)
	return redirect("/")

@login_required
def updateRecommendations(request):
	allStocks = Stock.objects.all()
	for stock in allStocks:
		stock.recommended = anal_rectum(stock.code)
		stock.save()
	return redirect('/')

def anal_rectum(symbol):
	timeDiff = datetime.timedelta(weeks=2) #two weeks in the past
	pastDate = datetime.datetime.now() - timeDiff
	currDate = datetime.datetime.now()

	url = "http://ichart.yahoo.com/table.csv?s="
	url += symbol
	url += "&a=" + str(pastDate.month - 1)
	url += "&b=" + str(pastDate.day)
	url += "&c=" + str(pastDate.year)
	url += "&d=" + str(currDate.month - 1)
	url += "&e=" + str(currDate.day)
	url += "&f=" + str(currDate.year)

	url += "&g=d&ignore=.csv"

	try:
		histData = urlopen(url) #file like object...read with file reader
		data = histData.read()
		
		rows = str(data).split('\\n')

		rising = 0
		falling = 0

		for row in rows[1:]:
			members = row.split(',')
			if(len(members) > 3):
				popen = float(members[1])
				pclose = float(members[4])

				if pclose-popen > 0:
					rising+=1
				else:
					falling+=1

		return rising > falling

	except URLError as e:
		return e