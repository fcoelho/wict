#coding: utf-8

from django.shortcuts import render

def index(request):
	return render(request, 'wict/index.html', {'home_active': True})

def articles(request):
	return render(request, 'wict/articles.html', {'articles_active' : True})

def registration(request):
	return render(request, 'wict/registration.html', {'registration_active' : True})

#@require_reviewer
#def review(request):
#	return render(request, 'wict/review.html', {'review_active' : True})

