from django.contrib import admin
from .models import ID, OTP, Appointment, User, NextOfKin
from django.contrib.auth.admin import UserAdmin


# Create a custom user admin class
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number','is_staff', 'date_joined','last_login', 'last_logout', 'active',)
    list_filter = ('is_Student_Patient', 'is_Staff_Patient', 'is_Doctor', 'is_staff', 'next_of_kin', 'username', 'last_login', 'last_logout','has_next_of_kin', 'first_name', 'last_name', 'email', 'patient_id', 'gender', 'phone_number', 'specialization','date_joined', 'active',)
    search_fields = ('username', 'first_name', 'last_name', 'email', 'specialization', 'gender', 'phone_number', 'patient_id')
    ordering = ('date_joined',)
    
    actions = ['deactivate_users', 'activate_users']
    
    # Custom actions
    def deactivate_users(self, request, queryset):
        queryset.update(active=False)
    deactivate_users.short_description = "Deactivate selected users"
    
    def activate_users(self, request, queryset):
        queryset.update(active=True)
    activate_users.short_description = "Activate selected users"
    
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'is_Student_Patient',
                    'is_Staff_Patient',
                    'is_Doctor',
                )
            }
        )
    )
    
admin.site.register(User, CustomUserAdmin)


# Register models
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appoint_id', 'appointee', 'appointed_doctor', 'appoint_area', 'book_time', 'approve_date', 'appoint_time',  'appoint_status', )
    ordering = ('book_time',)
    list_filter = ('appoint_id', 'appoint_area', ('appointed_doctor', admin.RelatedOnlyFieldListFilter), ('appointee', admin.RelatedOnlyFieldListFilter), 'appoint_status', 'appoint_time', 'book_time', 'is_resolved', 'approve_date', 'close_date') 
    
    search_fields = ('appoint_id', 
                     'book_time',
                     'appoint_time',
                     'appoint_area', 
                     'appoint_status',
                     'appointee__first_name',
                     'appointee__last_name', 
                     'appointee__patient_id',
                     'appointee__patient_type', 
                     'appointee__gender',
                     'appointee__email',
                     'appointee__phone_number',
                     'appointee__username',
                     'appointed_doctor__gender',
                     'appointed_doctor__first_name',
                     'appointed_doctor__last_name',
                     'appointed_doctor__username', 
                     'appointed_doctor__phone_number',
                     'appointed_doctor__email',  
                     'appointed_doctor__specialization',  
    )  
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'appointed_doctor':
            kwargs["queryset"] = User.objects.filter(is_Doctor=True)
        elif db_field.name == 'appointee':
            kwargs["queryset"] = User.objects.filter(is_Student_Patient=True) | User.objects.filter(is_Staff_Patient=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_phone')
    list_filter = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_phone')
    list_display = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_phone')
    search_fields = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_phone')
    
    
@admin.register(ID)
class IDAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'patient_type', 'registered')
    list_filter = ('patient_id', 'patient_type', 'registered')
    
    search_fields = ('patient_id', 'patient_type', 'registered')

    
class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp_code', 'otp_created', 'otp_verified', 'for_email')
    list_filter = ('otp_code', 'otp_verified', 'otp_created', 'for_email',)
    search_fields = ('otp_code','otp_verified', 'otp_created', 'for_email')
    readonly_fields = ('otp_code',  'otp_created', 'otp_verified', 'for_email')
    
admin.site.register(OTP, OTPAdmin)