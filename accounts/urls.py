from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('complete-profile/', views.complete_owner_profile, name='complete_owner_profile'),
    path('settings/', views.settings_view_page, name='settings'),
    
    path('password_reset_local/', views.password_reset_local, name='password_reset_local'),
    path('password_reset_complete/', views.password_reset_complete_local, name='password_reset_complete'),


    path('password_reset/',
            auth_views.PasswordResetView.as_view(
                template_name = 'registration/password_reset_form.html',
                email_template_name = 'registration/password_reset_email.html',
                subject_template_name = 'registration/password_reset_subject.txt',
                success_url = '/password_reset/done/',
            ),
            name ='password_reset'
        ),

    path('password_reset/done/',
            auth_views.PasswordResetDoneView.as_view(
                template_name= 'registration/password_reset_done.html'
            ),
            name='password_reset_done'
        ),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/',
            auth_views.PasswordResetCompleteView.as_view(
                template_name='registration/password_reset_complete.html'
            ),
            name = 'password_reset_complete'
        ),
]