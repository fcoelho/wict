from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from website.decorators import require_reviewer

from .models import Review
from .forms import ReviewFormSet, EvaluationForm

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
	
	if request.method == 'POST':
		formset = ReviewFormSet(request.POST, instance=review)
		evaluation = EvaluationForm(request.POST, instance=review.evaluation)
		if formset.is_valid() and evaluation.is_valid():
			formset.save()
			evaluation.save()
			return redirect('website_reviews')
	else:
		formset = ReviewFormSet(instance=review)
		evaluation = EvaluationForm(instance=review.evaluation)

	return render(request, 'wict/display_review.html',
		{
			'review': review,
			'formset': formset,
			'evaluation': evaluation
		}
	)

