from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

from website.decorators import require_reviewer

from .models import Review
from .forms import ReviewFormSet

@require_reviewer
def reviews(request):
	review_list = Review.objects.filter(reviewer=request.user)
	return render(request, 'wict/reviews.html', {'reviews': review_list})

@require_reviewer
def display_review(request, review_id):
	review_id = int(review_id)

	review = get_object_or_404(Review, pk=review_id)
	# check that the review belongs to the logged in reviewer
	if review.reviewer != request.user:
		return HttpResponseForbidden("403 Forbidden")


	formset  = ReviewFormSet(instance=review)

	return render(request, 'wict/display_review.html', {'review': review, 'formset': formset})

