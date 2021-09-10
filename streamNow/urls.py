from django.urls import path
from .views import (
    HomePage,
    MediaDetailView,
    PostCreateView
)
from . import views

urlpatterns = [
    path('', HomePage.as_view(), name='streamNow-home'),
    path('<str:media_type>/<int:_id>/', MediaDetailView.as_view(), name='media-detail'),
    path('<str:media_type>/<int:_id>/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='streamNow-about'),
    path('search/', views.search, name='streamNow-search')
]