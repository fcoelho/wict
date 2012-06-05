# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

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
