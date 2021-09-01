from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='streamNow-home'),
    path('about/', views.about, name='streamNow-about'),
    path('search/', views.search, name='streamNow-search')

]