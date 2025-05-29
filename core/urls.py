from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('register/complete-profile/', views.complete_owner_profile, name='complete_owner_profile'),
]