from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('compose/', views.compose, name='compose'),
    path('explore/', views.explore, name='explore'),
    path('explore/<str:value>/', views.explore_profile, name='explore_profile'),
    path('search/<str:value>/', views.search_results, name='searchresults'),
    path('notification/', views.notification, name='notification'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('about/', views.about, name='about'),
]