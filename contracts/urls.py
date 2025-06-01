from django.urls import path
from . import views

app_name = 'Contracts'

urlpatterns = [
    path('', views.contract_list, name='contract_list'),
    path('add/', views.contract_create, name='contract_create'),
    path('edit/<int:pk>/', views.contract_update, name='contract_update'),
    path('delete/<int:pk>/', views.contract_delete, name='contract_delete'),

    path('pdf/<int:pk>/', views.generate_contract_pdf, name='generate_contract_pdf'),
]
