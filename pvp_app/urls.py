from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pvp/', views.analyze, name='analyze'),
    path('search/<str:pokemon>', views.search, name='search'),
    path('evolutions/<str:pokemon>', views.get_evolutions, name='get_evolutions')
]