from django.urls import path
from . import views

urlpatterns = [
    path('agent_home/', views.agent_home),
    path('agent_register/', views.agent_register),
    path('agent_login/', views.agent_login),
    path('agent_logout/', views.agent_logout),
    path('material_view/', views.material_view),
    path('to_process/<int:id>/', views.to_process),
    path('progress_bar/', views.progress_bar),
    path('analyse/', views.analyse),
    path('apply_algorithm/<int:id>/', views.apply_algorithm),
    path('residue_page/', views.residue_page),
    path('create_residue/<int:id>/', views.create_residue),
]
