from datetime import timedelta
from account.models import Appointment
from . import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from .models import Payment
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from .models import Payment

# Create a view to initiate payment
@login_required
def initiate_payment(request: HttpRequest, appoint_id) -> HttpResponse:
    appointment = get_object_or_404(Appointment, appoint_id=appoint_id)
    
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST, user=request.user)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.appointment = appointment
            payment.patient = str(request.user)
            payment.amount = 2
            payment.email = request.user.email
            payment.save()
            return render(request, 'payments/make_payment.html', {'payment': payment, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = forms.PaymentForm(user=request.user)
    return render(request, 'payments/initiate_payment.html', {'payment_form': payment_form})


@login_required
# Create a view to verify payment
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    try:
        payment = get_object_or_404(Payment, ref=ref)
        verified = payment.verify_payment()
        
        if verified:
            # Update the appointment's payment, approve_date, and appoint_status fields
            appointment = payment.appointment
            appointment.payment = True
            appointment.appoint_status = 'Scheduled'
            appointment.approve_date = payment.date_created
            appointment.save()

            # Add 3 hours to the appointment time
            adjusted_appoint_time = appointment.appoint_time + timedelta(hours=3)
            
            # Send an email to the doctor
            doctor = appointment.appointed_doctor
            subject = 'New Appointment Scheduled'
            email_from = settings.EMAIL_HOST_USER
            message = (f"Dear Dr. {doctor.first_name.title()} {doctor.last_name.title()},\n\nA new appointment {appointment.appoint_id} "
                       f"has been scheduled with you. It's scheduled for {adjusted_appoint_time.strftime('%I:%M %p, %d %B %Y')}. "
                       f"Please make effort to be present on that day. Your appointment starts in {(adjusted_appoint_time - (timezone.now() + timedelta(hours=3))).days} days. "
                       "Appoint Master™ Appoint Master©2024 | All Rights reserved.")
            send_mail(subject, message, email_from, [doctor.email])

            # Send an email to the patient
            patient = appointment.appointee
            subject = 'Your Appointment Has Been Scheduled'
            email_from = settings.EMAIL_HOST_USER
            message = (f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} with doctor "
                       f"{doctor.first_name.title()} {doctor.last_name.title()} has been approved. It's scheduled for "
                       f"{adjusted_appoint_time.strftime('%I:%M %p, %d %B %Y')}. Please make effort to be present on that day. Your appointment starts in "
                       f"{(adjusted_appoint_time - (timezone.now() + timedelta(hours=3))).days} days. "
                       "Appoint Master™ Appoint Master©2024 | All Rights reserved.")
            send_mail(subject, message, email_from, [patient.email])
        
        else:
            if payment.appointment:
                # Update the appointment's appoint_status field
                appointment = payment.appointment
                appointment.appoint_status = 'Failed'
                appointment.is_resolved = True
                appointment.close_date = appointment.book_time
                appointment.save()
                
                # Send an email to the patient
                patient = appointment.appointee
                subject = 'Appointment Failed'
                email_from = settings.EMAIL_HOST_USER
                message = (f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} "
                           "has failed. Please try again. Appoint Master™ Appoint Master©2024 | All Rights reserved.")
                send_mail(subject, message, email_from, [patient.email])
                
            return render(request, 'payments/payment_failed.html')
        return render(request, 'payments/payment_success.html')
    
    except Exception as e:
        messages.error(request, "Oops! An error occurred while verifying the payment. Please try again later.")
        return redirect('home')  # Redirect to home page if an error occurs