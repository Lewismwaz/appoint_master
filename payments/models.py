from django.db import models
import secrets
from django.utils import timezone
from .paystack import PayStack


# Create a Payment model (PayStack Integration)
class Payment(models.Model):
    patient = models.CharField(max_length=30, default="")
    amount = models.PositiveBigIntegerField()
    appointment = models.ForeignKey('account.Appointment', on_delete=models.CASCADE, blank=True, null=True, related_name='payments')
    ref = models.CharField(max_length=100)
    receipt_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        ordering = ['-date_created',]
        
    def __str__(self) -> str:
        return f"KES: {self.amount}--- ID: {self.receipt_number}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        return self.amount * 100
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        print(result)
        if status:
            self.receipt_number = result['receipt_number']  # Fetching receipt number from result dictionary
            authorization = result.get('authorization', {})  # Fetch authorization details
            self.phone_number = f"{authorization.get('bin', '')}{authorization.get('last4', '')}"  # Combine bin and last4
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
            return self.verified  # Returning verification status
        else:
            return False
        