from django.contrib import admin
from django.urls import path, include
from .views import main_dashboard, table
#llama el /app/main 
#se nombra el main_dashboard que llama de views

urlpatterns = [
    path('main/', main_dashboard, name="main_dashboard"),
    
    path('table/', table, name='table'),

]
