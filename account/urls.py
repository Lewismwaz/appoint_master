from django.urls import path, include
from account import views
from appoint_app.views import dashboard, home, terms
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('export_user_payments_pdf/', views.export_user_payments_pdf, name='export_user_payments_pdf'),
    path('export_admin_all_payments_pdf/', views.export_admin_all_payments_pdf, name='export_admin_all_payments_pdf'),
    path('account/export_appointment_pdf/<str:appointment_id>/', views.export_appointment_pdf, name='export_appointment_pdf'),
    
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
    path('delete_account_confirmation/', views.delete_account_confirmation, name='delete_account_confirmation'),
    
    path('export/appointments_payments/pdf/', views.export_appointments_payments_pdf, name='export_appointments_payments_pdf'),
    
    path('doctor-otp-verification/', views.doctor_otp_verification, name='doctor_otp_verification'),
    path('admin-otp-verification/', views.admin_otp_verification, name='admin_otp_verification'),

    path('update-next-kin/<str:patient_username>/', views.update_patient_next_kin, name='update-next-kin'),
    path('update-patient-next-kin/<str:patient_username>/', views.update_patient_next_kin, name='update-patient-next-kin'),
    path('delete-next-of-kin/', views.delete_next_of_kin, name='delete-next-of-kin'),
    
    path("all-payments/", views.view_payments_patient, name='all-payments'),
    path("user-payments/", views.view_all_payments, name='user-payments'),
    path("manage-user-payments/", views.all_payments, name='manage-user-payments'),
    
    # path('create-appointment/next-of-kin/', views.create_appointment_next_of_kin, name='create-appointment-next-of-kin'),
    
    path("approved-appointments/", views.approved_appointments, name='approved-appointments'),
    path("create-appointment-patient/", views.create_appointment_patient, name='create-appointment-patient'),
    path("view-appointments-manage/", views.view_appointments_manage, name='view-appointments-manage'),
    path("appointments-list/", views.all_appointments, name='appointments_list'),
    path("appointments-list-doctor/", views.all_appointments_doctor, name='appointments_list_doctor'),
    path("view-appointments/", views.view_appointments, name='view-appointments'),
    path("view-all-appointments/", views.view_all_appointments, name='view-all-appointments'),
    path("view-all-appointments-doctor/", views.view_all_appointments_doctor, name='view-all-appointments-doctor'),
    path("view-appointment-patient/<str:appointment_id>/", views.view_appointment_patient, name='view-appointment-patient'),
    path("view-appointment/<str:appointment_id>/", views.view_appointment, name='view-appointment'),
    path("close-appointment/<str:appointment_id>/", views.close_appointment, name='close-appointment'),
    path("close-appointment-doctor/<str:appointment_id>/", views.close_appointment_doctor, name='close-appointment-doctor'),
    path("closed-appointments/", views.closed_appointments, name='closed-appointments'),
    path("cancel-appointment/<str:appointment_id>/", views.cancel_appointment, name='cancel-appointment'),
    path("cancel-patient-appointment/<str:appointment_id>/", views.cancel_patient_appointment, name='cancel-patient-appointment'),
    path("delete-appointment/<str:appointment_id>/", views.delete_appointment, name='delete-appointment'),
    path("delete-patient-appointment/<str:appointment_id>/", views.delete_patient_appointment, name='delete-patient-appointment'),
    path("video-call-patient/", views.video_call_patient, name='video-call-patient'),
    path("vide-call/", views.video_call, name='video-call'),
    
    path("", dashboard, name='dashboard'),
    path("home/", home, name='home'), 
    path('terms/', terms, name='terms'),
    
    path("update-doctor-profile/<str:doctor_username>/", views.update_doctor_profile, name='update-doctor-profile'),
    path("update-admin-profile/<str:admin_username>/", views.update_admin_profile, name='update-admin-profile'),
    path("update-patient-profile/<str:patient_username>/", views.update_patient_profile, name='update-patient-profile'),
    
    path('admins-portal/', TemplateView.as_view(template_name='appoint_app/admins_portal.html'), name='admins_portal'),
    path('doctors-portal/', TemplateView.as_view(template_name='appoint_app/doctors_portal.html'), name='doctors_portal'),
    path('student-patients-portal/', TemplateView.as_view(template_name='appoint_app/student_patients_portal.html'), name='student_patients_portal'),
    path('staff-patients-portal/', TemplateView.as_view(template_name='appoint_app/staff_patients_portal.html'), name='staff_patients_portal'),
     
    path('register-doctor/', views.register_doctor, name='register-doctor'),
    path('register-patient/', views.register_patient, name='register-patient'),
    path('register-patient-admin/', views.register_patient_admin, name='register-patient-admin'),
    path('register-admin/', views.register_admin, name='register-admin'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path("", include('django.contrib.auth.urls')),
]