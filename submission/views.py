from django.shortcuts import render, redirect

from website.decorators import require_author
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
		article = Article.objects.get(user=request.user)
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
		article = Article.objects.get(user=request.user)
	except Article.DoesNotExist:
		return redirect('website_submission')
	
	article.delete()
	return redirect('website_submission')
	
