from functools import wraps
from rest_framework import status
from rest_framework.response import Response
#https://devdojo.com/piovincecang/django-decorators-for-permissions-checks
from django.http import HttpResponseRedirect
from django.urls import reverse

def permit_if_role_in(allowed_roles=()):
    """ This decorator takes arguments and returns a Closure that utilizes these arguments. """

    def view_wrapper_function(decorated_view_function):
        """ This intermediate wrapper function takes the decorated View function (e.g. get, post) itself. """
    
        @wraps(decorated_view_function)
        def enforce_user_permissions(view, request, *args, **kwargs):
            """ A function that intercepts the View function and enforces permissions """
            # Perform permissions checking here, before control is passed to the View function that was decorated
            permissions_evaluations = map(lambda role: getattr(request.user, role, False), allowed_roles)
            is_authorized = any(permissions_evaluations)
            # if not is_authorized:
                
                # return HttpResponseRedirect("/")
                # return Response("You are authenticated but unauthorized!", status=status.HTTP_403_FORBIDDEN)
        
            
            # Passing the arguments and control over to the view function that was decorated
            response =  decorated_view_function(view, request, *args, **kwargs)

            # Perform actions here after the control is returned by the view function that was decorated
            
            return response
    
        return enforce_user_permissions
    
    return view_wrapper_function