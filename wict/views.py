#coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login
from django.core.exceptions import PermissionDenied
from django.conf import settings

from sendfile import sendfile

from wict.decorators import require_reviewer, require_submitter
from wict.models import Article
from wict.forms import ArticleForm

def index(request):
	return render(request, 'wict/index.html', {'home_active': True})

def articles(request):
	return render(request, 'wict/articles.html', {'articles_active' : True})

def registration(request):
	return render(request, 'wict/registration.html', {'registration_active' : True})

@require_submitter
def submission(request):
	article = Article.objects.filter(user=request.user)
	context = {'article' : article, 'submission_active' : True}
	return render(request, 'wict/submission.html', context)

@require_submitter
def new_submission(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			return HttpResponse('Form valido!')
	else:
		form = ArticleForm()
	
	context = {'form' : form, 'submission_active' : True}
	return render(request, 'wict/new_submission.html', context)

@require_reviewer
def review(request):
	return render(request, 'wict/review.html', {'review_active' : True})

#Não faz sentido alguém tentar fazer login se já logou antes,
#então se a pessoa estiver logada, redireciona pra outro lugar
def wict_login(request, **kwargs):
	if request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
	else:
		return login(request, **kwargs)

