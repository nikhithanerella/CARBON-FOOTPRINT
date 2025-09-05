from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('',views.dashboard,name='dashboard'),
    path('predict/',views.predict,name='predict'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
]
