import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from appoint_app.pdf import html2pdf
from .forms import AdminRegistrationForm, CreateAppointmentForm_patient, DoctorRegistrationForm, NextOfKinForm, PatientRegistrationForm_Admin, PatientRegistrationForm, UpdateProfileForm_admin, UpdateProfileForm_doctor, UpdateProfileForm_patient
from payments.models import Payment
from .models import ID, OTP, Appointment, NextOfKin, User
from django.utils import timezone
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.template.loader import get_template
from django.http import FileResponse
from xhtml2pdf import pisa
from io import BytesIO

def export_appointments_payments_pdf(request):
    appointments = Appointment.objects.all().order_by('-appoint_time')
    data = []
    for appointment in appointments:
        patient = appointment.appointee
        approved = appointment.approve_date if appointment.approve_date else "--"
        scheduled = appointment.appoint_time if appointment.appoint_time else "--"
        closed = appointment.close_date if appointment.close_date else "--"
        patient_type = "Student" if patient.is_Student_Patient else "Staff" if patient.is_Staff_Patient else "None"
        payment = Payment.objects.filter(appointment=appointment).first()
        payment_display = "Verified" if payment and payment.verified else "Failed"
        
        data.append([appointment.appoint_id, appointment.appoint_area, patient, patient_type, appointment.appointed_doctor, appointment.book_time, approved, scheduled, closed, appointment.appoint_status, payment_display])
    
    template_path = 'appoint_app/appointments_payments_report.html'
    context = {'data': data}
    template = get_template(template_path)
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return FileResponse(BytesIO(result.getvalue()), as_attachment=True, filename='All Appointments.pdf')
    else:
        return HttpResponse('Error Rendering PDF', status=400)
    
    
def appointment_pdf(request, appoint_id):
    
    appointments = Appointment.objects.all()
    for appointment in appointments:
        if appointment.appoint_id == appoint_id:
            context = {
                'appoint_id': appointment.appoint_id,
                'appoint_area': appointment.appoint_area,
                'appointee': appointment.appointee,
                'appointed_doctor': appointment.appointed_doctor,
                'book_time': appointment.book_time,
                'appoint_time': appointment.appoint_time,
                'approve_date': appointment.approve_date,
                'close_date': appointment.close_date,
                'appoint_status': appointment.appoint_status,
                'payment': appointment.payment,
                'is_resolved': appointment.is_resolved,
                'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
            }
            break
    else:
        return HttpResponse('Appointment not found!', status=404)
    
    # context = {
    #     'appointments': appointments,
    #     'user': request.user,
    #     'logo_path': os.path.join(settings.STATIC_ROOT, 'images', 'logo.png')
    #     }

    pdf = html2pdf('appoint_app/appointment_report.html', context)
    
    return pdf
    


def check_email_exists(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})

def toggle_dark_mode(request):
    if request.method == "POST" and request.user.is_authenticated:
        dark_mode = request.POST.get("darkMode")
        # Save the user's preference for dark mode in the session or database
        request.session["dark_mode"] = dark_mode
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)     


def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

  

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.active:
                login(request, user)
                user.set_last_login()  # Update last login time
                # Redirect users based on their roles
                if user.is_Staff_Patient:
                    return redirect('staff_patients_portal')
                elif user.is_Student_Patient:
                    return redirect('student_patients_portal')
                elif user.is_Doctor:
                    # Generate OTP and send it to the doctor's email
                    otp = OTP.objects.create(otp_code=OTP.generate_otp(), for_email=user.email)
                    send_mail_otp(user.email, otp.otp_code)
                    request.session['otp'] = otp.pk  # Store OTP id in session for verification
                    return redirect('doctor_otp_verification')  # Redirect to OTP verification page
                else:
                    # Generate OTP and send it to the admin's email
                    otp = OTP.objects.create(otp_code=OTP.generate_otp(), for_email=user.email)
                    send_mail_otp(user.email, otp.otp_code)
                    request.session['otp'] = otp.pk  # Store OTP id in session for verification
                    return redirect('admin_otp_verification')  # Redirect to OTP verification page
            else:
                # User account is inactive, prevent login
                messages.error(request, "Appoint Master is currently unavailable. Will be back soon...!")
                return render (request, 'appoint_app/login.html')
        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect('login') 

    return render(request, "appoint_app/login.html")

# Function to send OTP to the user's email
def send_mail_otp(email, otp):
    subject = 'OTP Verification Code'
    message = f'Your OTP for login is: {otp}'
    email_from = settings.EMAIL_HOST_USER  # Assuming EMAIL_HOST_USER is defined in your settings.py
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

# OTP verification view for doctors
def doctor_otp_verification(request):
    if request.method == 'POST':
        entered_otp = ''.join(request.POST.get(f'digit{i+1}') for i in range(6))  # Concatenate digits to form OTP
        otp_id = request.session.get('otp')
        if otp_id:
            otp = OTP.objects.get(pk=otp_id)
            if entered_otp == otp.otp_code:
                otp.otp_verified = True
                otp.save()
                del request.session['otp']  # Remove OTP from session after successful verification
                return redirect('doctors_portal')  # Redirect to admin's dashboard
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                # Pass the error messages to the template context
                error_messages = messages.get_messages(request)
                return render(request, 'appoint_app/doctor_otp_verification.html', {'error_messages': error_messages})
        else:
            # Handle case where there is no OTP stored in session
            return redirect('login')
    return render(request, 'appoint_app/doctor_otp_verification.html')

# OTP verification view for admins
def admin_otp_verification(request):
    if request.method == 'POST':
        entered_otp = ''.join(request.POST.get(f'digit{i+1}') for i in range(6))  # Concatenate digits to form OTP
        otp_id = request.session.get('otp')
        if otp_id:
            otp = OTP.objects.get(pk=otp_id)
            if entered_otp == otp.otp_code:
                otp.otp_verified = True
                otp.save()
                del request.session['otp']  # Remove OTP from session after successful verification
                return redirect('admins_portal')  # Redirect to admin's dashboard
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                # Pass the error messages to the template context
                error_messages = messages.get_messages(request)
                return render(request, 'appoint_app/admin_otp_verification.html', {'error_messages': error_messages})
        else:
            # Handle case where there is no OTP stored in session
            return redirect('login')
    return render(request, 'appoint_app/admin_otp_verification.html')


def delete_account_confirmation(request):
    if request.method == 'POST':
        try:
            # Attempt to delete the user account
            user = request.user
            user.delete()   
            
            # Send email to the registered patient
            subject = 'EAppoint Master'
            message = f'Your account has been permanently deleted!\nWe are sad to see you leave Appoint Master!\n\nThe E-Appoint Master™\n\t\tAppoint Master©2024 | All Rights reserved.'
            send_mail(subject, message, 'youremail@gmail.com', [user.email]) 
                   
            messages.error(request, 'Your account has been permanently deleted!')
            logout(request)  # Logout the user after deletion
            return redirect('login')  # Redirect to login or appropriate page
        except Exception as e:
            # Handle any exceptions that occur during account deletion
            messages.error(request, 'An error occurred while deleting your account! Please try again later.')
            return redirect('delete_account_confirmation')  # Redirect back to confirmation page if deletion fails
    else:
        # If the request method is not POST, display the confirmation page
        return render(request, "appoint_app/delete_account_confirmation.html")


def logout_user(request):
    user = request.user
    logout(request)
    user.set_last_logout()  # Update last logout time
    messages.success(request, 'Logout Success!')
    return redirect('login')
    


# """For Patients"""
def register_patient(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.save()
            
            # Send email to the registered patient
            subject = 'EAppoint Master'
            message = f'Welcome to Appoint Master {user.username}!\nDear {user.patient_type} patient, you are one step away from booking your first Doctor Appointment.\nThat is not all! You can even request for a video call with your Doctor today!\nJoin thousands of Appoint Master users NOW!\n\nDo LOG INTO YOUR ACCOUNT AND UPDATE YOUR PROFILE.\nThe E-Appoint Master™\n\t\tAppoint Master©2024 | All Rights reserved.'
            send_mail(subject, message, 'youremail@gmail.com', [user.email])
            
            messages.success(request, ('Your Account has been created successfully!'))
            return redirect('login')
        
    else:
        form = PatientRegistrationForm()   
    return render(request, "appoint_app/register_patient.html", {'form':form})



def validate_patient_id(patient_id):
    try:
        patient = ID.objects.get(id=patient_id)
        # Check if the patient ID exists and is associated with a valid user
        if patient.user.is_active:
            return True
        else:
            return False
    except ID.DoesNotExist:
        return False




def create_appointment_patient(request):
    user = request.user
    
    # Check if the request method is POST
    if request.method == "POST":
        
        # Check if the user already has a scheduled appointment
        if Appointment.objects.filter(appointee=request.user, appoint_status='Scheduled').exists():
            messages.error(request, "You have a scheduled appointment! You cannot book a new appointment at the moment.")
            return redirect('create-appointment-patient')

        # If no scheduled appointments, proceed to create a new appointment
        form = CreateAppointmentForm_patient(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.appointee = user
            instance.appoint_status = 'Failed'
            instance.is_resolved = False
            
            doctor = User.objects.filter(specialization=instance.appoint_area).first()
            if doctor:
                instance.appointed_doctor = doctor
                instance.save()
                
                # Send an email to the patient
                patient = user
                appointment = instance  
                subject = 'Your Appointment Request Has Been Submitted'
                message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment request {appointment.appoint_id} with doctor {doctor.first_name.title()} {doctor.last_name.title()} has been submitted. Appoint Master™ Appoint Master©2024 | All Rights reserved."
                send_mail(subject, message, 'youremail@gmail.com', [patient.email])

                return redirect('initiate-payment', appoint_id=instance.appoint_id)
            
            else:
                messages.error(request, "No doctor for requested area is currently available for booking! Try again later.")
                return render(request, "appoint_app/create_appointment_patient.html", {'form': form})
            
        else:
            messages.error(request, "Oops! Ensure you entered everything correctly, then try again.")
            return render(request, "appoint_app/create_appointment_patient.html", {'form': form})
    
    else:
        form = CreateAppointmentForm_patient(user=request.user)
    
    return render(request, "appoint_app/create_appointment_patient.html", {'form': form})


def view_appointment_patient(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)
    appointment.payment_display = "Verified" if appointment.payment else "N/A"
    return render(request, 'appoint_app/view_appointment_patient.html', {'appointment': appointment})


def view_appointments(request):
    # Filter appointments based on the logged-in user
    user = request.user
    user_appointments = Appointment.objects.filter(appointee=user)
    patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
    for appointment in user_appointments:
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number 
        appointment.payment_display = "Verified" if appointment.payment else "N/A"
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"
    
    return render(request, 'appoint_app/view_appointments.html', {'user_appointments': user_appointments, 'patient_type':patient_type})


def view_payments_patient(request):
    # Filter payments based on the logged-in user
    user = request.user
    user_payments = Payment.objects.filter(patient=user)
    patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
    for payment in user_payments:
        payment.patient_type = patient_type
        payment.verified_display = "Yes" if payment.verified else "No" 
    
    return render(request, 'appoint_app/view_payments.html', {'user_payments': user_payments, 'patient_type':patient_type})



def view_appointments_manage(request):
     # Filter appointments based on the logged-in user
    user = request.user
    all_user_appointments = Appointment.objects.filter(appointee=user)
    patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
    for appointment in all_user_appointments:
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number 
        appointment.payment_display = "Verified" if appointment.payment else "N/A"
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"

    return render(request, 'appoint_app/view_appointments_manage.html', {'all_user_appointments': all_user_appointments, 'patient_type':patient_type})

     
def video_call_patient(request):
    pass
    return render(request, "appoint_app/video_call_patient.html")      
  


def update_patient_profile(request, patient_username):
    user = request.user
    profile = get_object_or_404(User, username=patient_username)
    if request.method == 'POST':
        form = UpdateProfileForm_patient(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update success!')
            return render(request, 'appoint_app/update_patient_profile.html', {'profile': profile, 'form': form})
        else:
            return render(request, 'appoint_app/update_patient_profile.html', {'profile': profile, 'form': form})
    else:
        form = UpdateProfileForm_patient(instance=profile)
    return render(request, 'appoint_app/update_patient_profile.html', {'profile': profile, 'form': form})


def update_patient_next_kin(request, patient_username):
    user = request.user
    next_of_kin = None
    try:
        next_of_kin = NextOfKin.objects.get(related_patient=user)
    except NextOfKin.DoesNotExist:
        pass

    if request.method == 'POST':
        form = NextOfKinForm(request.POST, instance=next_of_kin)
        if form.is_valid():
            print("Form is valid.")  # Debug statement
            next_of_kin = form.save(commit=False)
            next_of_kin.related_patient = user
            print("Form data:", form.cleaned_data)  # Debug statement
            next_of_kin.save()
            user.has_next_of_kin = True
            user.save()
            messages.success(request, 'Next of Kin details updated successfully!')
            return redirect('update-patient-profile', patient_username=user.username)
        else:
            print("Form errors:", form.errors)  # Debug statement
    else:
        form = NextOfKinForm(instance=next_of_kin)
    
    return render(request, 'appoint_app/next_kin.html', {'next_of_kin_form': form})



def delete_next_of_kin(request):
    if request.method == 'POST':
        next_of_kin = NextOfKin.objects.filter(related_patient=request.user).first()
        if next_of_kin:
            next_of_kin.delete()
            # Update user's has_next_of_kin field
            request.user.has_next_of_kin = False
            request.user.save()
            messages.success(request, 'Next of Kin details deleted successfully!')
        else:
            messages.error(request, 'No Next of Kin found to delete.')
        
    return redirect('update-patient-profile', patient_username=request.user.username)


      

""" For Doctors (Admin) """ 
def register_patient_admin(request):
    if request.method == "POST":
        admin_form = PatientRegistrationForm_Admin(request.POST)
        if admin_form.is_valid():
            user = admin_form.save(commit=False)
            user.is_patient = True
            user.save()
            
            # Send email to the registered patient
            subject = 'Accounts.Admin'
            message = f'Your Patient Account has been successfully created!\nPatient Type: {user.patient_type}.\nYour Patient ID:{user.patient_id}\n\nHere are your login details:\nUsername: {user.username}\nPassword: {admin_form.cleaned_data["password1"]}\n\nPlease LOG INTO YOUR ACCOUNT AND UPDATE YOUR PROFILE.\nThe E-Appoint Master™\n\t\tAppoint Master©2024 | All Rights reserved.'
            send_mail(subject, message, 'youremail@gmail.com', [user.email])
            
            messages.success(request, ('Patient Account has been created successfully!'))
            return render(request, "appoint_app/register_patient_admin.html", {'admin_form':admin_form})
        
    else:
        admin_form = PatientRegistrationForm_Admin()   
    return render(request, "appoint_app/register_patient_admin.html", {'admin_form':admin_form})
        

def register_doctor(request):
    if request.method == "POST":
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_Doctor = True
            user.save()
            
            # Send email to the registered patient
            subject = 'Accounts.Admin'
            message = f'Your Doctor Account has been successfully created!\nYour Specialization: {user.specialization}.\n\nHere are your login details:\nUsername: {user.username}\nPassword: {form.cleaned_data["password1"]}\n\nPlease LOG INTO YOUR ACCOUNT AND UPDATE YOUR PROFILE.\nThe E-Appoint Master™\n\t\tAppoint Master©2024 | All Rights reserved.'
            send_mail(subject, message, 'youremail@gmail.com', [user.email])
            
            messages.success(request, ('Doctor Account has been created successfully!'))
            return render(request, "appoint_app/register_doctor.html", {'form':form})
        
    else:
        form = DoctorRegistrationForm()   
    return render(request, "appoint_app/register_doctor.html", {'form':form})


def register_admin(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form.save()
            
            # Send email to the registered patient
            subject = 'Accounts.Admin'
            message = f'Your Admin Account has been successfully created!\n\nHere are your login details:\nUsername: {user.username}\nPassword: {form.cleaned_data["password1"]}\n\nPlease LOG INTO YOUR ACCOUNT AND UPDATE YOUR PROFILE.\nThe E-Appoint Master™\n\t\tAppoint Master©2024 | All Rights reserved.'
            send_mail(subject, message, 'youremail@gmail.com', [user.email])
            
            
            messages.success(request, 'Admin account has been created successfully!')
            return render(request, "appoint_app/register_admin.html", {'form': form})
    else:
        form = AdminRegistrationForm()
    return render(request, "appoint_app/register_admin.html", {'form': form})



def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)
    user = appointment.appointee
    patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
    phone_number = user.phone_number
    appointee = f"{user.first_name} {user.last_name}"
    appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"
    appointment.payment_display = "Verified" if appointment.payment else "N/A"
    return render(request, 'appoint_app/view_appointment.html', {'appointment': appointment, 'patient_type': patient_type, 'phone_number': phone_number, 'appointee':appointee})

 

def view_all_appointments(request):
    appointments_list = Appointment.objects.all().order_by('-appoint_time')
    
    for appointment in appointments_list:
        user = appointment.appointee
        patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number
        appointment.payment_display = "Verified" if appointment.payment else "N/A"
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No" 

    return render(request, 'appoint_app/view_all_appointments.html', {'appointments_list': appointments_list})



def view_all_appointments_doctor(request):
    doctor = request.user  # Get the logged-in doctor
    # Filter appointments based on the logged-in doctor's specialization or appointments assigned to the doctor
    appointments_list = Appointment.objects.filter(appoint_area=doctor.specialization) | Appointment.objects.filter(appointed_doctor=doctor).order_by('-appoint_time')
    
    for appointment in appointments_list:
        user = appointment.appointee
        patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number 
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"
        appointment.appointed_doctor = doctor  # Assign the logged-in doctor to appointed_doctor
        
    return render(request, 'appoint_app/view_all_appointments_doctor.html', {'appointments_list': appointments_list})


def all_appointments_doctor(request):
    doctor = request.user  # Get the logged-in doctor
    # Filter appointments based on the logged-in doctor's specialization or appointments assigned to the doctor
    appointments_list = Appointment.objects.filter(appoint_area=doctor.specialization) | Appointment.objects.filter(appointed_doctor=doctor).order_by('-appoint_time')
    
    for appointment in appointments_list:
        user = appointment.appointee
        patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number 
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"
        appointment.appointed_doctor = doctor  # Assign the logged-in doctor to appointed_doctor

    return render(request, 'appoint_app/view_appointments_list_doctor.html', {'appointments_list': appointments_list})


# Manage all Appointments
def all_appointments(request):   
    appointments_list = Appointment.objects.all().order_by('-appoint_time')

    for appointment in appointments_list:
        user = appointment.appointee
        patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number 
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"
        appointment.payment_display = "Verified" if appointment.payment else "N/A"

    return render(request, 'appoint_app/view_appointment_list.html', {'appointments_list': appointments_list})
  
  
def view_all_payments(request):   
    all_user_payments = Payment.objects.filter(user=request.user).order_by('-date_created')
    

    for payment in all_user_payments: 
        payment.verified_display = "Yes" if payment.verified else "No"

    return render(request, 'appoint_app/view_payments_admin.html', {'all_user_payments': all_user_payments})    

  
    
# Manage all user Payments
def all_payments(request):   
    all_user_payments = Payment.objects.all().order_by('-date_created')

    for payment in all_user_payments: 
        payment.verified_display = "Yes" if payment.verified else "No"

    return render(request, 'appoint_app/view_payment_list.html', {'all_user_payments': all_user_payments})    
    



def approved_appointments(request):
    doctor = request.user  # Get the logged-in doctor
    
    # Filter appointments based on the logged-in doctor's specialization or appointments assigned to the doctor
    appointments_list = Appointment.objects.filter(appoint_area=doctor.specialization) | Appointment.objects.filter(appointed_doctor=doctor).order_by('-appoint_time')
    
    # Filter appointments to include only approved appointments
    approved_appointments = appointments_list.filter(payment='True')
    
    # Process additional data for each appointment, if necessary
    for appointment in approved_appointments:
        user = appointment.appointee
        patient_type = "Student" if user.is_Student_Patient else "Staff" if user.is_Staff_Patient else "None"
        appointment.patient_type = patient_type
        appointment.phone_number = user.phone_number 
        appointment.is_resolved_display = "Yes" if appointment.is_resolved else "No"
        appointment.appointed_doctor = doctor  # Assign the logged-in doctor to appointed_doctor
        
    return render(request, 'appoint_app/approved_appointments.html', {'appointments': approved_appointments})



def closed_appointments(request):
    appointments = Appointment.objects.filter(appointed_doctor=request.user, is_resolved=True, appoint_status__in=['Failed', 'Completed', 'Canceled']).order_by('-appoint_time')
    
    for appointment in appointments:
        appointee = appointment.appointee
        patient_type = "Student" if appointee.is_Student_Patient else "Staff" if appointee.is_Staff_Patient else "None"
        appointment.patient_type = patient_type
    
    return render(request, "appoint_app/closed_appointments.html", {'appointments': appointments})



def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the cancellation
        appointment.appoint_status = "Canceled"
        appointment.is_resolved = True
        appointment.close_date = timezone.now()
 
        appointment.save()  
        
        # Send an email to the doctor
        doctor = appointment.appointed_doctor
        subject = 'Appointment Cancelled'
        message = f"Dear Dr. {doctor.last_name.title()},\n\nThe appointment {appointment.appoint_id} has been cancelled. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [doctor.email])

        # Send an email to the patient
        patient = appointment.appointee
        subject = 'Your Appointment Has Been Cancelled'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} with doctor {doctor.first_name.title()} {doctor.last_name.title()} has been cancelled. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])
    
        
        messages.success(request, 'Appointment has been cancelled successfully.')
        return redirect('appointments_list')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/cancel_appointment.html', {'appointment': appointment})


def cancel_patient_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the cancellation
        appointment.appoint_status = "Canceled"
        appointment.is_resolved = True
        appointment.close_date = timezone.now()
 
        appointment.save() 
        
        # Send an email to the doctor
        doctor = appointment.appointed_doctor
        subject = 'Appointment Cancelled'
        message = f"Dear Dr. {doctor.last_name.title()},\n\nThe appointment {appointment.appoint_id} has been cancelled. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [doctor.email])

        # Send an email to the patient
        patient = appointment.appointee
        subject = 'Your Appointment Has Been Cancelled'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} with doctor {doctor.first_name.title()} {doctor.last_name.title()} has been cancelled. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])
        
        messages.success(request, 'Appointment has been cancelled successfully.')
        return redirect('view-appointments-manage')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/cancel_patient_appointment.html', {'appointment': appointment})


def cancel_doctor_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the cancellation
        appointment.appoint_status = "Canceled"
        appointment.is_resolved = True
        appointment.close_date = timezone.now()
        
        print(appointment.appoint_status, appointment.close_date)  # Before saving
        appointment.save()
        print(appointment.appoint_status, appointment.close_date)  
        
        # Send an email to the doctor
        doctor = appointment.appointed_doctor
        subject = 'Appointment Cancelled'
        message = f"Dear Dr. {doctor.last_name.title()},\n\nThe appointment {appointment.appoint_id} has been cancelled. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [doctor.email])

        # Send an email to the patient
        patient = appointment.appointee
        subject = 'Your Appointment Has Been Cancelled'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} with doctor {doctor.first_name.title()} {doctor.last_name.title()} has been cancelled. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])
        
        messages.success(request, 'Appointment has been cancelled successfully.')
        return redirect('appointments_list_doctor')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/cancel_doctor_appointment.html', {'appointment': appointment})
  

def close_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the cancellation
        appointment.appoint_status = "Completed"
        appointment.is_resolved = True
        appointment.close_date = timezone.now()
        
        appointment.save()  
        
        # Send an email to the doctor
        doctor = appointment.appointed_doctor
        subject = 'Appointment Completed'
        message = f"Dear Dr. {doctor.last_name.title()},\n\nThe appointment {appointment.appoint_id} has been completed. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [doctor.email])

        # Send an email to the patient
        patient = appointment.appointee
        subject = 'Your Appointment Has Been Completed'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} with doctor {doctor.first_name.title()} {doctor.last_name.title()} has been completed. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])

        
        messages.success(request, 'Appointment has been completed successfully.')
        return redirect('appointments_list')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/close_doctor_appointment.html', {'appointment': appointment})


def close_appointment_doctor(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the cancellation
        appointment.appoint_status = "Completed"
        appointment.is_resolved = True
        appointment.close_date = timezone.now()
        
        appointment.save()  
        
        # Send an email to the doctor
        doctor = appointment.appointed_doctor
        subject = 'Appointment Completed'
        message = f"Dear Dr. {doctor.last_name.title()},\n\nThe appointment {appointment.appoint_id} has been completed. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [doctor.email])

        # Send an email to the patient
        patient = appointment.appointee
        subject = 'Your Appointment Has Been Completed'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} with doctor {doctor.first_name.title()} {doctor.last_name.title()} has been completed. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])

        
        messages.success(request, 'Appointment has been completed successfully.')
        return redirect('appointments_list_doctor')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/close_doctor_appointment.html', {'appointment': appointment})
  

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the delete
        deleted_appointment_id = appointment.appoint_id
        
        # Send an email to the patient
        patient = appointment.appointee
        subject = f'Your Appointment {appointment.appoint_id} Has Been Deleted'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} has been deleted. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])

        appointment.delete()
        
        messages.error(request, f'Appointment {deleted_appointment_id} has been deleted.')
        return redirect('appointments_list')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/delete_appointment.html', {'appointment': appointment})  


def delete_patient_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appoint_id=appointment_id)

    if request.method == 'POST':
        # If the user confirms the delete
        deleted_appointment_id = appointment.appoint_id
        
        # Send an email to the patient
        patient = request.user
        subject = f'Your Appointment {appointment.appoint_id} Has Been Deleted'
        message = f"Hello, {patient.first_name.title()} {patient.last_name.title()}! Your appointment {appointment.appoint_id} has been deleted. Appoint Master™ Appoint Master©2024 | All Rights reserved."
        send_mail(subject, message, 'youremail@gmail.com', [patient.email])

        appointment.delete()
        
        messages.success(request, f'Your appointment {deleted_appointment_id} has been deleted.')
        return redirect('view-appointments-manage')  # Redirect to a page after cancellation

    return render(request, 'appoint_app/delete_patient_appointment.html', {'appointment': appointment})  
      
      
def video_call(request):
    pass
    return render(request, "appoint_app/video_call.html")



def update_doctor_profile(request, doctor_username):
    user = request.user
    profile = get_object_or_404(User, username=doctor_username)
    if request.method == 'POST':
        form = UpdateProfileForm_doctor(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update success!')
            return render(request, 'appoint_app/update_doctor_profile.html', {'profile': profile, 'form': form})
        else:
            messages.error(request, 'Failed to update profile! Check form, then try again.')
            return render(request, 'appoint_app/update_doctor_profile.html', {'profile': profile, 'form': form})
    else:
        form = UpdateProfileForm_doctor(instance=profile)
    return render(request, 'appoint_app/update_doctor_profile.html', {'profile': profile, 'form': form})



def update_admin_profile(request, admin_username):
    profile = get_object_or_404(User, username=admin_username)
    if request.method == 'POST':
        form = UpdateProfileForm_admin(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update success!')
            return render(request, 'appoint_app/update_admin_profile.html', {'profile': profile, 'form': form})
        else:
            messages.error(request, 'Failed to update profile! Check form, then try again.')
            return render(request, 'appoint_app/update_admin_profile.html', {'profile': profile, 'form': form})
    else:
        form = UpdateProfileForm_admin(instance=profile)
    return render(request, 'appoint_app/update_admin_profile.html', {'profile': profile, 'form': form})


