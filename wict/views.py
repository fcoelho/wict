#coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login
from django.core.exceptions import PermissionDenied

from sendfile import sendfile

from wict.decorators import require_reviewer, require_submitter

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

@require_submitter
def submission(request):
	return render_to_response(
		'wict/submission.html',
		RequestContext(request)
	)

@require_reviewer
def review(request):
	return render_to_response(
		'wict/review.html',
		RequestContext(request)
	)

#Não faz sentido alguém tentar fazer login sem logou antes,
#então se a pessoa estiver logada, redireciona pra '/'
def wict_login(request, **kwargs):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return login(request, **kwargs)

