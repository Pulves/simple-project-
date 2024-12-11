from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('user/register/', views.register, name='register' ),
    path('user/login/', views.login, name='login'),
    path('user/all/', views.get_all_users, name='all_users'),
]