from django.urls import path
from . import views

urlpatterns = [
    path('environment_home/', views.environment_home),
    path('environment_register/', views.environment_register),
    path('environment_login/', views.environment_login),
    path('environment_logout/', views.environment_logout),
]
