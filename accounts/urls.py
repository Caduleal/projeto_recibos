from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('complete-profile/', views.complete_owner_profile, name='complete_owner_profile'),

]