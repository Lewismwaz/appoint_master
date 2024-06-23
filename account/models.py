from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
import string
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db.models import Q


# Create a Custom User Model   
class User(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
   
    PATIENT_TYPE_CHOICES = [
        ('', '-----'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('', '----------'),
        ('Dentistry', 'Dentistry'),
        ('Pharmacy', 'Pharmacy'),       
        ('Consultation', 'Consultation'),
        ('Flu Treatment', 'Flu Treatment'),
        ('ENT', 'Ear, Nose, and Throat (ENT)'),
        ('Reproductive Health', 'Reproductive Health'),
        ('Mental Health', 'Mental Health'),
        ('Physiotherapy', 'Physiotherapy'),
        ('Covid-Screening', 'Covid-19 Screening'),
        ('VCT', 'HIV Counselling & Treatment'),
        ('Laboratory', 'Laboratory Tests'),
        ('Referral', 'Referral'),
        ('Other issue', 'Other issue'),]
    
    is_Student_Patient = models.BooleanField(default=False)
    is_Staff_Patient = models.BooleanField(default=False)
    has_next_of_kin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    next_of_kin = models.ForeignKey('NextOfKin', on_delete=models.CASCADE, blank=True, null=True)
    is_Doctor = models.BooleanField(default=False)
    specialization = models.CharField(max_length=19, blank=False, choices=SPECIALIZATION_CHOICES)
    profile_photo = models.ImageField(upload_to='Profile-photos/', null=True, blank=True)
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPE_CHOICES)
    patient_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="")
    phone_number = PhoneNumberField(max_length=13, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    def set_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def set_last_logout(self):
        self.last_logout = timezone.now()
        self.save(update_fields=['last_logout'])
    
    def populate_username(self):
        if self.patient_id:
            self.username = self.patient_id.username
            self.save()
    
    def next_of_kin_name(self):
        if self.has_next_of_kin:
            try:
                next_of_kin = NextOfKin.objects.get(related_patient=self)
                return f"{next_of_kin.kin_fname} {next_of_kin.kin_lname}"
            except NextOfKin.DoesNotExist:
                return "None"
        else:
            return "None"
        
    # Meta class to set metadata options
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Create a model for Next of Kin(for a Patient)
class NextOfKin(models.Model):
    RELATIONSHIP_CHOICES = [
        ('', '----------'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Aunt', 'Aunt'),
        ('Uncle', 'Uncle'),
        ('Niece', 'Niece'),
        ('Nephew', 'Nephew'),
        ('Cousin', 'Cousin'),
        ('Other close Relative', 'Other close Relative'),
        ('Wife', 'Wife'),
        ('Husband', 'Husband'),
        ('Guardian', 'Guardian'),
    ]

    kin_fname = models.CharField(max_length=50)
    kin_lname = models.CharField(max_length=50)
    related_patient = models.ForeignKey(
    User,
    verbose_name='Related Patient',
    on_delete=models.CASCADE,
    limit_choices_to=Q(is_Student_Patient=True) | Q(is_Staff_Patient=True)
)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    kin_phone = PhoneNumberField(max_length=13, blank=True, null=True, unique=False)

    def __str__(self):
        return f"{self.kin_fname} {self.kin_lname}"
    
    class Meta:
        verbose_name = "Next of Kin"
        verbose_name_plural = "Next of Kins"


# Create a model for Patient ID(Student & Staff)
class ID(models.Model):
    PATIENT_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Staff', 'Staff'),
    ]
    patient_id = models.CharField(max_length=15, unique=True)
    patient_type = models.CharField(max_length=50, choices=PATIENT_TYPE_CHOICES)
    registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient_type} ID: {self.patient_id}"
    
    class Meta:
        verbose_name = "Patient ID"
        verbose_name_plural = "Patient IDs"


# Create a method to generate a random appointment ID
def generate_appointment_id():
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choices(alphanumeric, k=6))


# Create a model for Appointment
class Appointment(models.Model):
    APPOINTMENT_AREA_CHOICES = (
        ('', '----------'),
        ('Dentistry', 'Dentistry'),
        ('Pharmacy', 'Pharmacy'),       
        ('Consultation', 'Consultation'),
        ('Flu Treatment', 'Flu Treatment'),
        ('ENT', 'Ear, Nose, and Throat (ENT)'),
        ('Reproductive Health', 'Reproductive Health'),
        ('Mental Health', 'Mental Health'),
        ('Physiotherapy', 'Physiotherapy'),
        ('Covid-Screening', 'Covid-19 Screening'),
        ('VCT', 'HIV Counselling & Treatment'),
        ('Laboratory', 'Laboratory Tests'),
        ('Referral', 'Referral'),
        ('Other issue', 'Other issue'),
    )
     
    APPOINTMENT_STATUS_CHOICES = (
        ('', '-----'),
        ('Failed', 'Failed'),
        ('Scheduled', 'Scheduled'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed'),    
    )
    
    FOR_CHOICES = [
        ('', '-----'),
        ('self', 'Self'),
        ('next_of_kin', 'Next of Kin'),
    ]
    
    RESOLVED_CHOICES = [
    (True, 'Yes'),
    (False, 'No'),]
    
    PAYMENT_CHOICES = [
    (True, 'Verified'),
    (False, 'N/A'),]
    
    payment = models.BooleanField('Payment', default=False, blank=True, null=True, choices=PAYMENT_CHOICES)
    appoint_id = models.CharField('Appointment ID', primary_key=True, max_length=6, default=generate_appointment_id, editable=False)
    appoint_area = models.CharField('Area', max_length=19, blank=False, choices=APPOINTMENT_AREA_CHOICES)
    appointee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients', blank=False)
    appointed_doctor = models.ForeignKey(User, blank=True, null=True, related_name="Doctors", on_delete=models.SET_NULL)
    book_time = models.DateTimeField('Booked on', default=timezone.now, editable=False)
    approve_date = models.DateTimeField('Approved on', blank=True, null=True)
    appoint_time = models.DateTimeField('Appointed Date', blank=True, null=True)
    doctor_remarks = models.CharField('Remarks', max_length=100, blank=True, null=True)
    is_resolved = models.BooleanField('Is resolved', default=False, blank=True, null=True, choices=RESOLVED_CHOICES)
    close_date = models.DateTimeField('Closed on', blank=True, null=True)
    appoint_status = models.CharField('Status', max_length=10, choices=APPOINTMENT_STATUS_CHOICES, blank=False)

    # Save method to set the book time & appoint ID
    def save(self, *args, **kwargs):
        if not self.pk:  # Only set the book time if it's a new appointment
            self.book_time = timezone.now()
        self.full_clean()  # Validate model fields before saving
        super().save(*args, **kwargs)  # Call the "real" save() method

    def __str__(self):
        return self.appoint_id


# Create a model for OTP(One Time Password)    
class OTP(models.Model):
    otp_code = models.CharField(max_length=6)
    otp_created = models.DateTimeField(default=timezone.now)
    otp_verified = models.BooleanField(default=False)
    for_email = models.EmailField(null=True, blank=True, default="")

    @classmethod
    def generate_otp(cls):
        return ''.join(random.choices('0123456789', k=6))
    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
    