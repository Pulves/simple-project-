from django.urls import path
from . import views

urlpatterns = [
    path('post/feed/', views.feed, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('notification/', views.notifications, name='notifications' )
]