from django.contrib.auth.decorators import user_passes_test, login_required
			
def require_reviewer(function):
	is_reviewer = user_passes_test(lambda u: u.is_reviewer)
	return login_required(is_reviewer(function))

def require_author(function):
	is_author = user_passes_test(lambda u: not u.is_reviewer)
	return login_required(is_author(function))

