from django.urls import path, include
from . import views

urlpatterns = [


    path('profiles/<str:account>', views.myProfile, name="myProfile"),
    path('follow/<int:id>', views.follow, name="follow")
]