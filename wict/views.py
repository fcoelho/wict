#coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from sendfile import sendfile

def index(request):
	return render_to_response(
		'wict/index.html',
		RequestContext(request)
	)

def articles(request):
	return render_to_response(
		'wict/articles.html',
		RequestContext(request)
	)

def registration(request):
	return HttpResponse('registration')

@login_required
def submission(request):
	return HttpResponse('submission')

@login_required
def review(request):
	return HttpResponse('review')

#Não faz sentido alguém tentar fazer login sem logou antes,
#então se a pessoa estiver logada, redireciona pra '/'
def wict_login(request, **kwargs):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return login(request, **kwargs)
