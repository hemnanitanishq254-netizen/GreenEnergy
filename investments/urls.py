from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/invest/', views.invest, name='invest'),
    path('my-investments/', views.my_investments, name='my_investments'),
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
]