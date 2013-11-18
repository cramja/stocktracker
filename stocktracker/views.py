from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def index(response):
	return render(response, 'index.html')

def visuals(response):
	return render(response, 'visuals.html')