from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse

def stocks(request):
	return render(request, "stocks/stocks.html")