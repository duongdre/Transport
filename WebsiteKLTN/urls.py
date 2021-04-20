from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('map/', views.map),
    path('account/', views.account),
    path('history/', views.history),
    path('directionConfirm/', views.directionConfirm),
    path('profile/', views.profile),
    path('transport/', views.transport),
    path('viewHistory/', views.viewHistory),
    path('test/', views.test),
]