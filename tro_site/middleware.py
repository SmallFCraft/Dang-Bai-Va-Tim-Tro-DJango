"""
Custom middleware for error handling
"""
from django.shortcuts import render
from django.http import Http404
from django.conf import settings


class CustomErrorHandlerMiddleware:
    """
    Middleware to show custom error pages even in DEBUG mode
    Set SHOW_CUSTOM_ERROR_PAGES = True in settings to enable
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only override if setting is enabled
        if not getattr(settings, 'SHOW_CUSTOM_ERROR_PAGES', False):
            return response
        
        # Handle 404 responses
        if response.status_code == 404:
            return render(request, 'errors/404.html', status=404)
        
        # Handle 500 responses (only if not in DEBUG or explicitly enabled)
        if response.status_code == 500 and not settings.DEBUG:
            return render(request, 'errors/500.html', status=500)
        
        return response
    
    def process_exception(self, request, exception):
        """Handle exceptions and show custom error pages"""
        # Only override if setting is enabled
        if not getattr(settings, 'SHOW_CUSTOM_ERROR_PAGES', False):
            return None
        
        if isinstance(exception, Http404):
            return render(request, 'errors/404.html', status=404)
        
        # For 500 errors, only catch in production or if explicitly enabled
        if settings.DEBUG:
            return None
        
        return render(request, 'errors/500.html', status=500)
