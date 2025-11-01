from django.urls import path
from . import views

urlpatterns = [
    path('deligator_home/', views.deligator_home),
    path('deligator_login/', views.deligator_login),
    path('deligator_logout/', views.deligator_logout),
    path('raw_materials/', views.raw_materials),
    path('send_raw_details/', views.send_raw_details),
    path('materials_sent/<int:id>/', views.materials_sent),
    path('res_details/', views.res_details),
    path('statistics/', views.statistics),
    path('stati/', views.stati),
]

