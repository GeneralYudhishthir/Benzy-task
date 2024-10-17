from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.get_canteen_report, name='canteen_report'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.user_login, name='login'), 
]


