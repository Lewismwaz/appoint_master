from django.contrib import admin
from .models import Payment
from django.utils import timezone

# Create a class to display the Payment model in the Admin interface
class PaymentAdmin(admin.ModelAdmin):
    def date(self, obj):
        if obj.date_created:
            return timezone.localtime(obj.date_created)
        return None

    list_display = ('receipt_number', 'amount', 'phone_number', 'date_created',  'appointment','patient', 'email', 'verified')
    list_filter = ('receipt_number', 'amount', 'phone_number',  'date_created',  'appointment','patient', 'email', 'verified')
    search_fields = ('receipt_number', 'amount', 'phone_number',  'date_created', 'appointment','patient', 'email', 'verified',)
admin.site.register(Payment, PaymentAdmin)