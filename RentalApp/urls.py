from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('accounts.urls')),

    path('tenants/', include(('tenants.urls', 'Tenant'), namespace='Tenant')),
    path('properties/', include('properties.urls', namespace='Properties')),
    path('contracts/', include('contracts.urls', namespace='Contracts')),
    path('payments/', include('payments.urls', namespace='Payments')),
]
