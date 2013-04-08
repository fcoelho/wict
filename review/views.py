from django.shortcuts import render

from website.decorators import require_reviewer

from .models import Review

@require_reviewer
def reviews(request):
	review_list = Review.objects.filter(reviewer=request.user)
	return render(request, 'wict/reviews.html', {'reviews': review_list})
