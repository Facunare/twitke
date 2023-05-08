from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
urlpatterns = [
    path('landing/', views.landingPage, name="landingPage"),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('accounts/', include('allauth.urls')),
    path('signup-google/', views.signup_google, name='signup_google'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")
]