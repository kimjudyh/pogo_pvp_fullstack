from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pvp/', views.analyze, name='analyze'),
]