
from django.contrib import admin
from django.urls import path, include 
from report import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('report.urls')),
]
