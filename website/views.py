#coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.conf import settings
from django.core.urlresolvers import reverse

from sendfile import sendfile

from wict.decorators import require_reviewer, require_submitter
from wict.models import Article, Author
from wict.forms import ArticleForm, AuthorForm, AuthorFormSet

def index(request):
	return render(request, 'wict/index.html', {'home_active': True})

def articles(request):
	return render(request, 'wict/articles.html', {'articles_active' : True})

def registration(request):
	return render(request, 'wict/registration.html', {'registration_active' : True})

@require_submitter
def submission(request):
	try:
		#Só pode existir um artigo com esse usuário, então bora lá
		article = Article.objects.get(user=request.user)
		authors = []
		for author in Author.objects.filter(article=article):
			authors.append(author.first_name + ' ' + author.last_name)
	except:
		article = None
		authors = None
	context = {
		'article' : article,
		'authors' : authors,
		'submission_active' : True
	}
	return render(request, 'wict/submission.html', context)

@require_submitter
def new_submission(request):
	if Article.objects.filter(user=request.user).exists():
		return HttpResponseRedirect(reverse('submission'))
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save(commit=False)
			article.user = request.user
			formset = AuthorFormSet(request.POST, instance=article)
			if formset.is_valid():
				article.save()
				formset.save()
				return HttpResponseRedirect(reverse('submission'))
		else:
			formset = AuthorFormSet(request.POST)
			
	else:
		form = ArticleForm()
		formset = AuthorFormSet(instance=Article())
	
	context = {'form' : form, 'formset' : formset, 'submission_active' : True}
	return render(request, 'wict/new_submission.html', context)

@require_submitter
def edit_submission(request):
	try:
		article = Article.objects.get(user=request.user)
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('submission_new'))
	
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES, instance=article)
		if form.is_valid():
			article = form.save()
			formset = AuthorFormSet(request.POST, instance=article)
			if formset.is_valid():
				article.save()
				formset.save()
				return HttpResponseRedirect(reverse('submission'))
		else:
			formset = AuthorFormSet(request.POST, instance=article)
	else:
		form = ArticleForm(instance=article)
		formset = AuthorFormSet(instance=article)
	
	context = {'form' : form, 'formset' : formset, 'submission_active' : True}
	return render(request, 'wict/edit_submission.html', context)

@require_submitter
def delete_submission(request):
	try:
		article = Article.objects.get(user=request.user)
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('submission'))
	
	article.delete()
	return HttpResponseRedirect(reverse('submission'))
	
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

