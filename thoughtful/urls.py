from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
]