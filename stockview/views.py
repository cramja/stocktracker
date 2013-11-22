from django.shortcuts import render, get_object_or_404, render_to_response

def index(request):
	return render(request, 'stockview/stockview.html')