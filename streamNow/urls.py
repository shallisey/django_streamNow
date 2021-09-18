from django.urls import path
from .views import (
    HomePage,
    PostListVIew,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchForm

)
from . import views

urlpatterns = [
    path('', HomePage.as_view(), name='streamNow-home'),
    path('<str:media_type>/<int:_id>/', PostListVIew.as_view(), name='post-list'),
    path('post/<str:media_type>/<int:_id>/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<str:media_type>/<int:_id>/new/', PostCreateView.as_view(), name='post-create'),  # Shares html with PostUpdateView post_form
    path('post/<str:media_type>/<int:_id>/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<str:media_type>/<int:_id>/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Looks for form <model>_confirm_delete
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name='streamNow-about'),
    path('search/', SearchForm.as_view(), name='search-form')
]