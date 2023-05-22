from django.contrib.auth.models import User
from profiles.models import Profiles

def random_users(request):
    random_users = []
    if request.user.is_authenticated:
        if request.user.is_authenticated and not request.user.is_staff:
            current_profile = Profiles.objects.get(user__username = request.user.username)
            random_users = Profiles.objects.exclude(id__in=current_profile.followed_users.values_list('id', flat=True)).exclude(id=request.user.id).order_by('?')[:5]
        

        
    return {'random': random_users}


def current_profile(request):
    current_profile = None  # Valor predeterminado

    if request.user.is_authenticated and not request.user.is_staff:
        current_profile = Profiles.objects.get(user__username=request.user.username)

    return {'current_profile': current_profile}
