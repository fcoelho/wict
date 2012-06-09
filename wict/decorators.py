from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def is_reviewer(user):
	profile = user.get_profile()
	if profile:
		return profile.is_reviewer
	else:
		raise Http404
			
def require_reviewer(function=None, login_url=None):
	def check_reviewer(user):
		if not user.is_authenticated():
			return False
		if is_reviewer(user):
			return True
		else:
			raise PermissionDenied
	decorator = user_passes_test(check_reviewer, login_url=login_url)
	if function:
		return decorator(function)
	else:
		return decorator

def require_submitter(function=None, login_url=None):
	def check_submitter(user):
		if not user.is_authenticated():
			return False
		if not is_reviewer(user):
			return True
		else:
			raise PermissionDenied
	decorator = user_passes_test(check_submitter, login_url=login_url)
	if function:
		return decorator(function)
	else:
		return decorator
		
