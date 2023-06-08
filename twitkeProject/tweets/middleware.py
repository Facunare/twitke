from django.shortcuts import redirect
from profiles.models import Profiles
from django.urls import reverse

class BannedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_profile = Profiles.objects.get(user__username=request.user.username)
            if current_profile.banned and not request.path.startswith(reverse('logout')) and not request.path.startswith(reverse('banned')) and not request.path.startswith('/unbanRequest/') and not request.path.startswith('/admin/'):
                return redirect('banned')

        response = self.get_response(request)
        return response
