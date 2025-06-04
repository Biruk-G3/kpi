from django.urls import path
from . import views
from .views import export_kpi_summary, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',    views.home, name="home"),
    path('export_kpi/', export_kpi_summary, name='export_kpi'),
    path('create_kpi/',      views.create_kpi, name="create_kpi"),
    path('add_progress/',    views.add_progress, name="add_progress"),
    path('kpi_summary/',     views.kpi_summary, name='kpi_summary'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]
