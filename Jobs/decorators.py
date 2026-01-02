from django.core.exceptions import PermissionDenied

def recruiter_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != "recruiter":
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def applicant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ["student", "professional"]:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
