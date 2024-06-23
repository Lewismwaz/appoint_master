from datetime import time
from django import forms
from .models import ID, NextOfKin, User, generate_appointment_id
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Appointment, User, NextOfKin
from django.core.exceptions import ValidationError

# Create form choices
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
        ('Other issue', 'Other issue'),
]

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

GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
RESOLVED_CHOICES = [
    (True, 'Yes'),
    (False, 'No'),
]

PATIENT_TYPE_CHOICES = [
    ('', '-----'),
    ('Student', 'Student'),
    ('Staff', 'Staff'),
]


# Create a custom password input widget with an eye icon to toggle password visibility
class PasswordInputWithToggle(PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        eye_toggle = '''
        <div class="relative">
            {}
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5">
                <button 
                    type="button" 
                    class="text-blue-500 hover:text-gray-700 focus:outline-none focus:shadow-outline-blue active:text-gray-800 toggle-password">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        </div>
        '''.format(rendered)
        return mark_safe(eye_toggle)


# Create a custom Admin user registration form
class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Email'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    password1 = forms.CharField(required=True, label='Password', widget=PasswordInput(attrs={'id': 'password', 'autocomplete': 'current-password', 'placeholder': 'Password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    password2 = forms.CharField(required=True, label='Confirm Password', widget=PasswordInput(attrs={'id': 'password2', 'autocomplete': 'new-password', 'placeholder': 'Confirm Password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user


# Create a custom Doctor registration form
class DoctorRegistrationForm(UserCreationForm):
    specialization = forms.ChoiceField(required=True, label='Specialization', choices=SPECIALIZATION_CHOICES, widget=forms.Select(attrs={'id': 'specialization', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Email'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    first_name = forms.CharField(label='First Name:', required=True, widget=forms.TextInput(attrs={'id': 'first_name', 'autocomplete': '', 'placeholder': 'First name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    last_name = forms.CharField(label='Last Name:', required=True, widget=forms.TextInput(attrs={'id': 'last_name', 'autocomplete': '', 'placeholder': 'Last name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    password1 = forms.CharField(required=True, label='Password', widget=PasswordInput(attrs={'id': 'password', 'autocomplete': 'current-password', 'placeholder': 'Password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    password2 = forms.CharField(required=True, label='Confirm Password', widget=PasswordInput(attrs={'id': 'password2', 'autocomplete': 'new-password', 'placeholder': 'Confirm Password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
        
    class Meta:
        model = User
        fields = ['username', 'specialization', 'first_name', 'last_name',  'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_Doctor = True
        if commit:
            user.save()
        return user


# Create a custom Patient(next-of-kin) registration form
class NextOfKinForm(forms.ModelForm):
    relationship = forms.ChoiceField(label='Relationship*', choices=NextOfKin.RELATIONSHIP_CHOICES, widget=forms.Select(attrs={'id': 'relationship', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))
    kin_fname = forms.CharField(label='First Name*', required=True, widget=forms.TextInput(attrs={'id': 'kin_fname', 'autocomplete': '', 'placeholder': 'First name...', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    kin_lname = forms.CharField(label='Last Name*', required=True, widget=forms.TextInput(attrs={'id': 'kin_lname', 'autocomplete': '', 'placeholder': 'Last Name...', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    kin_phone = PhoneNumberField(
        label='Phone Number[Optional]',
        required=False,
        max_length=13,
        widget=PhoneNumberPrefixWidget(attrs={
            'id': 'phoneInput',
            'name': 'phone_number',
            'type': 'tel',
            'autocomplete': 'tel',
            'placeholder': 'e.g. 0712345678',
            'required': False,
            'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
        }),
    )
    
    class Meta:
        model = NextOfKin
        fields = ['kin_fname', 'kin_lname', 'relationship', 'kin_phone']    


# Create a custom Patient registration form
class PatientRegistrationForm(UserCreationForm):
    patient_type = forms.ChoiceField(required=True, label='Patient Type', choices=PATIENT_TYPE_CHOICES, widget=forms.Select(attrs={'id': 'patient_type', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),)
    patient_id = forms.CharField(label='Patient ID', required=True, widget=forms.TextInput(attrs={'id': 'patient_id', 'autocomplete': '', 'placeholder': 'Enter your ID', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=15)
    phone_number = PhoneNumberField(
        label='Phone Number',
        max_length=13,
        widget=PhoneNumberPrefixWidget(attrs={
            'id': 'phoneInput',
            'name': 'phone_number',
            'type': 'tel',
            'autocomplete': 'tel',
            'placeholder': 'e.g. (+254) 712345678',
            'required': True,
            'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
        }),
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Enter your Email'}))
    first_name = forms.CharField(label='First Name:', required=True, widget=forms.TextInput(attrs={'id': 'first_name', 'autocomplete': '', 'placeholder': 'Enter your first name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    last_name = forms.CharField(label='Last Name:', required=True, widget=forms.TextInput(attrs={'id': 'last_name', 'autocomplete': '', 'placeholder': 'Enter your last name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Create your unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    password1 = forms.CharField(required=True, label='Password', widget=PasswordInputWithToggle(attrs={'id': 'password', 'autocomplete': 'current-password', 'placeholder': 'Create your password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    password2 = forms.CharField(required=True, label='Confirm Password', widget=PasswordInputWithToggle(attrs={'id': 'password2', 'autocomplete': 'new-password', 'placeholder': 'Confirm your password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    
    agree_to_terms = forms.BooleanField(
        label='Agree to Terms of Use & Privacy',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'id': 'agree_to_terms',
            'class': 'form-checkbox text-red h-9 w-9',
        }),
    )
    
    # Meta class to define the model and fields to be used in the form
    class Meta:
        model = User
        fields = ['username', 'patient_type',  'patient_id', 'first_name', 'last_name', 'email', 'phone_number',  'password1', 'password2', 'agree_to_terms']
    
    # Custom clean method to validate the patient ID
    def clean_patient_id(self):
        patient_id = self.cleaned_data.get('patient_id')
        patient_type = self.cleaned_data.get('patient_type')

        try:
            patient_record = ID.objects.get(patient_id=patient_id, patient_type=patient_type)
            if patient_record.registered:
                raise forms.ValidationError("The user ID is already registered!")
        except ID.DoesNotExist:
            raise forms.ValidationError("Invalid user ID")

        return patient_id

    # Custom save method to save the user and update the patient ID record
    def save(self, commit=True):
        user = super().save(commit=False)
        patient_type = self.cleaned_data.get('patient_type')
        patient_id = self.cleaned_data.get('patient_id')

        try:
            patient_record = ID.objects.get(patient_id=patient_id, patient_type=patient_type)
            if not patient_record.registered:
                patient_record.registered = True
                patient_record.save()
        except ID.DoesNotExist:
            pass
        
        if patient_type == 'Student':
            user.is_Student_Patient = True
        elif patient_type == 'Staff':
            user.is_Staff_Patient = True

        if commit:
            user.save()
        return user
    

# Create a custom Patient registration form for the Admin
class PatientRegistrationForm_Admin(UserCreationForm):
    patient_type = forms.ChoiceField(required=True, label='Patient Type', choices=PATIENT_TYPE_CHOICES, widget=forms.Select(attrs={'id': 'patient_type', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),)
    patient_id = forms.CharField(label='Patient ID', required=True, widget=forms.TextInput(attrs={'id': 'patient_id', 'autocomplete': '', 'placeholder': 'ID', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=15)
    first_name = forms.CharField(label='First Name:', required=True, widget=forms.TextInput(attrs={'id': 'first_name', 'autocomplete': '', 'placeholder': 'First name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    last_name = forms.CharField(label='Last Name:', required=True, widget=forms.TextInput(attrs={'id': 'last_name', 'autocomplete': '', 'placeholder': 'Last name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Email'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Create unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    password1 = forms.CharField(required=True, label='Password', widget=PasswordInputWithToggle(attrs={'id': 'password', 'autocomplete': 'current-password', 'placeholder': 'Create your password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    password2 = forms.CharField(required=True, label='Confirm Password', widget=PasswordInputWithToggle(attrs={'id': 'password2', 'autocomplete': 'new-password', 'placeholder': 'Confirm your password', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 pr-10'}))
    
    class Meta:
        model = User
        fields = ['username', 'patient_type',  'patient_id', 'first_name', 'last_name', 'email',  'password1', 'password2']
    
    def clean_patient_id(self):
        patient_id = self.cleaned_data.get('patient_id')
        patient_type = self.cleaned_data.get('patient_type')

        try:
            patient_record = ID.objects.get(patient_id=patient_id, patient_type=patient_type)
            if patient_record.registered:
                raise forms.ValidationError("The user ID is already registered!")
        except ID.DoesNotExist:
            raise forms.ValidationError("Invalid user ID")

        return patient_id

    def save(self, commit=True):
        user = super().save(commit=False)
        patient_type = self.cleaned_data.get('patient_type')
        patient_id = self.cleaned_data.get('patient_id')

        try:
            patient_record = ID.objects.get(patient_id=patient_id, patient_type=patient_type)
            if not patient_record.registered:
                patient_record.registered = True
                patient_record.save()
        except ID.DoesNotExist:
            pass
        
        if patient_type == 'Student':
            user.is_Student_Patient = True
        elif patient_type == 'Staff':
            user.is_Staff_Patient = True

        if commit:
            user.save()
        return user

    
# Create custom validation for the Datetime field for an appointment
class RestrictedDateTimeField(forms.DateTimeField):
    def validate(self, value):
        super().validate(value)
        if value:
            if value < timezone.now():  # Check if datetime is in the past
                raise ValidationError("Appointment cannot be scheduled in the past.")
            if value.weekday() > 4:  # Check if it's Saturday or Sunday
                raise ValidationError("Appointment can only be scheduled on Mondays to Fridays.")
            if value.time() < time(8, 0) or value.time() > time(17, 0):  # Check if time is outside 8am-5pm
                raise ValidationError("Appointment time should be between 8 am and 5 pm.")
            if time(12, 0) <= value.time() < time(14, 0):  # Check if time is between 12pm-2pm
                raise ValidationError("Appointment cannot be scheduled between 12 pm and 2 pm.")
            if value.minute not in [0, 30]:  # Check if minutes are either 00 or 30
                raise ValidationError("Appointment time should be on the hour or half past the hour.")

    
# Create a custom form for creating an appointment (by Patients)
class CreateAppointmentForm_patient(forms.ModelForm):           
    FOR_CHOICES = [
        ('', '-----'),
        ('self', 'Self'),
        ('next_of_kin', 'Next of Kin'),
    ]

    appoint_area = forms.ChoiceField(
    label='Appointment Area:',
    required=True,
    choices=Appointment.APPOINTMENT_AREA_CHOICES,
    widget=forms.Select(attrs={
        'id': 'appoint_area',
        'required': True,
        'class': 'block w-full mb-2 mt-2 rounded-full border-0 py-1.5 text-gray-800 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
    })
    )

    # Assign the RestrictedDateTimeField (with validation) to the appoint_time field
    appoint_time = RestrictedDateTimeField()
    
    class Meta:
        model = Appointment
        fields = ['appoint_area', 'appoint_time']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieve and store the user object
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.appoint_id = generate_appointment_id()
        if self.user:
            instance.appointee = self.user
        instance.book_time = timezone.now()
        instance.appoint_status = 'Failed'
        if commit:
            instance.save()
        return instance  


# Create a custom form to update Profile (by Patients)
class UpdateProfileForm_patient(forms.ModelForm):   
    profile_photo = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'hidden', 'accept': 'image/*',
        'id': 'profile_photo',
        'class': 'block w-full mt-2 mb-2 rounded-full border-0 border-none p-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent sm:text-sm'
    }))   
    first_name = forms.CharField(label='First Name:', required=True, widget=forms.TextInput(attrs={'id': 'first_name', 'autocomplete': '', 'placeholder': 'Enter your first name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    last_name = forms.CharField(label='Last Name:', required=True, widget=forms.TextInput(attrs={'id': 'last_name', 'autocomplete': '', 'placeholder': 'Enter your last name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    gender = forms.ChoiceField(label='Gender:', required=True, choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'id': 'gender', 'required': True, 'class': 'focus:ring-indigo-500 h-3 w-3 text-indigo-black text-semibold text-sm border-gray-300'}),)
    phone_number = PhoneNumberField(
        label='Phone Number:',
        max_length=13,
        widget=PhoneNumberPrefixWidget(attrs={
            'id': 'phoneInput',
            'name': 'phone_number',
            'type': 'tel',
            'autocomplete': 'tel',
            'placeholder': 'e.g. (+254) 712345678',
            'required': True,
            'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
        }),
    )
    email = forms.EmailField(required=True, label='Email:', widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Update your Email'}))
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Create your unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    
    class Meta:
        model = User
        fields = ['profile_photo','username', 'first_name', 'last_name', 'gender', 'email', 'phone_number']


# Create a custom form to update Profile (by Doctors)
class UpdateProfileForm_doctor(forms.ModelForm):  
    profile_photo = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'hidden', 'accept': 'image/*',
        'id': 'profile_photo',
        'class': 'block w-full mt-2 mb-2 rounded-full border-0 border-none p-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent sm:text-sm'
    }))
    first_name = forms.CharField(label='First Name:', required=True, widget=forms.TextInput(attrs={'id': 'first_name', 'autocomplete': '', 'placeholder': 'Enter your first name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    last_name = forms.CharField(label='Last Name:', required=True, widget=forms.TextInput(attrs={'id': 'last_name', 'autocomplete': '', 'placeholder': 'Enter your last name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    gender = forms.ChoiceField(label='Gender:', required=True, choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'id': 'gender', 'required': True, 'class': 'focus:ring-indigo-500 h-3 w-3 text-indigo-black text-semibold text-sm border-gray-300'}),)
    
    phone_number = PhoneNumberField(
        label='Phone Number:',
        max_length=13,
        widget=PhoneNumberPrefixWidget(attrs={
            'id': 'phoneInput',
            'name': 'phone_number',
            'type': 'tel',
            'autocomplete': 'tel',
            'placeholder': 'e.g. (+254) 712345678',
            'required': True,
            'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
        }),
    )
    email = forms.EmailField(required=True, label='Email:', widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Update your Email'}))
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Create your unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    
    class Meta:
        model = User
        fields = ['profile_photo', 'username', 'first_name', 'last_name', 'gender', 'email', 'phone_number']


# Create a custom form to update Profile (by Admin)
class UpdateProfileForm_admin(forms.ModelForm):  
    profile_photo = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'hidden', 'accept': 'image/*',
        'id': 'profile_photo',
        'class': 'block w-full mt-2 mb-2 rounded-full border-0 border-none p-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent sm:text-sm'
    }))
    first_name = forms.CharField(label='First Name:', required=True, widget=forms.TextInput(attrs={'id': 'first_name', 'autocomplete': '', 'placeholder': 'Enter your first name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    last_name = forms.CharField(label='Last Name:', required=True, widget=forms.TextInput(attrs={'id': 'last_name', 'autocomplete': '', 'placeholder': 'Enter your last name', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), max_length=50)
    email = forms.EmailField(required=True, label='Email:', widget=forms.EmailInput(attrs={'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 'id': 'email', 'autocomplete': 'email', 'placeholder': 'Update your Email'}))
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Create your unique username', 'required': True, 'class': 'block w-full rounded-full border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}), required=True)
    
    class Meta:
        model = User
        fields = ['profile_photo', 'username', 'first_name', 'last_name', 'email']