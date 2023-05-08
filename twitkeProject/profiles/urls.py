from django.urls import path, include
from . import views

urlpatterns = [


    path('profiles/<int:id>', views.myProfile, name="myProfile"),
    path('follow/<int:id>', views.follow, name="follow"),
    path('update/profiles/<int:id>', views.updateProfile, name="updateProfile"),
    path('verifyRequest/<int:id>,', views.verifyRequest, name="verifyRequest"),
    path('verifyRequest/<int:id>/delete,', views.deleteVerifyRequest, name="deleteVerifyRequest"),
]