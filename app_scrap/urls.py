from django.urls import path
from . import views

urlpatterns = [
    path('scrap_home/', views.scrap_home),
    path('scrap_register/', views.scrap_register),
    path('scrap_login/', views.scrap_login),
    path('scrap_logout/', views.scrap_logout),
    path('residue_details/', views.residue_details),
    path('residue_details_send/', views.residue_details_send),
    path('residue_send/<int:id>/', views.residue_send)
]
