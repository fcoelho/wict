# coding: utf-8

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from website.decorators import require_author
from website.utils import group_review_criteria
from review.models import Review
from .models import Article, Author
from .forms import ArticleForm, AuthorForm, AuthorFormSet

@require_author
def submission(request):
	try:
		article = Article.objects.get(author=request.user)
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

@require_author
def new_submission(request):
	if Article.objects.filter(author=request.user).exists():
		return redirect('website_submission')
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save(commit=False)
			article.author = request.user
			formset = AuthorFormSet(request.POST, instance=article)
			if formset.is_valid():
				article.save()
				formset.save()
				return redirect('website_submission')
		else:
			formset = AuthorFormSet(request.POST)
			
	else:
		form = ArticleForm()
		formset = AuthorFormSet(instance=Article())
	
	context = {'form' : form, 'formset' : formset, 'submission_active' : True}
	return render(request, 'wict/new_submission.html', context)

@require_author
def edit_submission(request):
	try:
		article = Article.objects.get(author=request.user)
	except Article.DoesNotExist:
		return redirect('website_submission_new')
	
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES, instance=article)
		if form.is_valid():
			article = form.save()
			formset = AuthorFormSet(request.POST, instance=article)
			if formset.is_valid():
				article.save()
				formset.save()
				return redirect('website_submission')
		else:
			formset = AuthorFormSet(request.POST, instance=article)
	else:
		form = ArticleForm(instance=article)
		formset = AuthorFormSet(instance=article)
	
	context = {'form' : form, 'formset' : formset, 'submission_active' : True}
	return render(request, 'wict/edit_submission.html', context)

@require_author
def delete_submission(request):
	try:
		article = Article.objects.get(author=request.user)
	except Article.DoesNotExist:
		return redirect('website_submission')
	
	article.delete()
	return redirect('website_submission')
	
@require_author
def show_comments(request):
	try:
		article = Article.objects.get(author=request.user)
	except Article.DoesNotExist:
		return redirect('website_submission')

	reviews = Review.objects.filter(article=article)
	reviews = filter(lambda x: x.reviewed(), reviews)
	if not reviews:
		messages.info(request, _(u'Você ainda não pode ver os comentários'))
		return redirect('website_submission')

	data_by_criterias = group_review_criteria(reviews)

	context = {
		'submission_active': True,
		'data_by_criterias': data_by_criterias,
	}

	return render(request, 'wict/comments_submission.html', context)

