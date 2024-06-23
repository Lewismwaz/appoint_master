from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account import views


urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path("", include('appoint_app.urls')),
    path("account/", include('account.urls')),
    path('secure-appoint-pay/', include('payments.urls')),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='appoint_app/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='appoint_app/password_reset_done.html'), name='password_reset_done'), 
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='appoint_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='appoint_app/password_reset_complete.html'), name='password_reset_complete'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
