from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from time import time
from thread import start_new_thread

from stocks.models import Stock
from stocks.recommend import *

updateAfter = 86400 # 1 day in seconds
lastRecommendationUpdate = 0

def index(request):
    global lastRecommendationUpdate
    if time() > lastRecommendationUpdate + updateAfter:
        lastRecommendationUpdate = time()
        start_new_thread(updateRecommendations, ())
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

def updateRecommendations():
    allStocks = Stock.objects.all()
    for stock in allStocks:
        stock.recommended = run_recommendation_analysis(stock)
        stock.save()
