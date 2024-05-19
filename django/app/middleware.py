# app/middleware.py
## @package app
#  Contains middleware components for the application.
#

## @file middleware
#  Implements middleware to handle role-based access control throughout the application.
#

from django.shortcuts import redirect
from django.urls import resolve

## Role-based access middleware that restricts access to URLs based on user roles.
#  This middleware intercepts requests and checks if the requested URL is forbidden for the user's role.
#  It uses a dictionary to define URLs that are inaccessible for each role.
#  If a user attempts to access a forbidden URL, they are redirected to a 'forbidden' page.
#
class RoleBasedAccessMiddleware:
    ## Initializes the middleware.
    #  @param get_response A callable to get the response for the current request.
    #  This method sets up the middleware with a response handler and a predefined list of forbidden URLs for each role.
    #
    def __init__(self, get_response):
        self.get_response = get_response
        self.forbidden_urls = {
            'T': ['/curator/', '/methodist/', '/admin/'],
            'C': ['/tutor/', '/methodist/', '/admin/'],
            'M': ['/tutor/', '/curator/', '/admin/'],
            'A': []
        }

    ## Middleware call method.
    #  @param request The HTTP request object.
    #  This method is called on every request, before determining which view should handle the request.
    #  It checks the user's role and the requested URL to determine if access should be restricted.
    #  If the URL is forbidden for the user's role, redirects to a 'forbidden' response.
    #
    def __call__(self, request):
        user_role = request.session.get('user_role')

        if user_role:
            current_url = request.path
            forbidden_urls_for_role = self.forbidden_urls.get(user_role, [])

            if any(current_url.startswith(url) for url in forbidden_urls_for_role):
                return redirect('forbidden')

        response = self.get_response(request)
        return response
