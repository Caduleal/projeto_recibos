from django.urls import path
from . import views

app_name = 'Tenant'

urlpatterns = [
    path('', views.tenant_list, name='tenant_list'),
    path('add/', views.tenant_create, name='tenant_form'),
    path('edit/<int:pk>/', views.tenant_update, name='tenant_update'),
    path('delete/<int:pk>/', views.tenant_delete, name='tenant_delete'),

    path('ajax/tenant-list-ajax/',views.tenant_list_ajax,name='tenant_list_ajax'),
]
