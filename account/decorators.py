from django.contrib.auth.decorators import user_passes_test


def logout_required(function=None, logout_url = "/accounts/profile/"):
    """
    Decorator for views that checks that the user is logged out, redirecting
    to the profile if there is a user loggedin
    """
    actual_decorator =  user_passes_test(
        lambda u: not u.is_authenticated,
        login_url= logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator