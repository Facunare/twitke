from django.urls import path, include
from . import views

from django.views.generic import TemplateView
urlpatterns = [
    path('landing/', views.landingPage, name="landingPage"),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('accounts/', include('allauth.urls'))
]