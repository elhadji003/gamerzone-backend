from django.urls import path
from . import views, views_like

urlpatterns = [
    path('all_posts/', views.GetAllPostGamings.as_view(), name='postgaming-list'),
    path('posts/', views.PostGamingListCreateView.as_view(), name='postgaming-list-create'),
    path('posts/<int:pk>/', views.PostGamingDetailView.as_view(), name='postgaming-detail'),
    path('posts/<int:post_id>/like/', views_like.like_post, name='like-post'), 
]
