from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pvp/', views.analyze, name='analyze'),
    path('search/<str:pokemon>', views.search, name='search'),
    path('evolutions/<str:pokemon>', views.get_evolutions, name='get_evolutions'),
    path('search/', views.empty_search, name='empty_search'),
    path('evolutions/', views.empty_evolution, name='empty_evolution')
]