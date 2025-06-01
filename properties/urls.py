from django.urls import path
from . import views

app_name = 'Properties'  

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('add/', views.property_create, name='property_form'),
    path('edit/<int:pk>/', views.property_update, name='property_update'),
    path('delete/<int:pk>/', views.property_delete, name='property_delete'),
]
