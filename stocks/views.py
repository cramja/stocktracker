from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
	return render(request, 'stocks/base.html')
	
def quotes(request):
	return render(request, 'stockview/quotes.html')
	
def login(request):
	return render(request, 'users/login.html')
	
def register(request):
	return render(request, 'users/register.html')