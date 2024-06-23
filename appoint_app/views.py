from django.shortcuts import redirect, render
from account.models import Appointment, User
from payments.models import Payment 
from django.contrib.auth import logout 
from django.contrib import messages


# Create a logout view
def logout_view(request):
    logout(request)
    if request.user.is_authenticated:
        request.user.set_last_logout()  # Update last logout time
        messages.success(request, 'Logout Success!')
    return redirect('login')



# Create a dashboard view
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_active and user.is_staff and user.is_superuser:
            # Calculate appointment statistics here
            payments = Payment.objects.all()
            students = User.objects.filter(is_Student_Patient=True)
            staff = User.objects.filter(is_Staff_Patient=True)
            
            mpesa = payments.count()
            students_cover = students.count()
            medicare = staff.count()
            appointments = Appointment.objects.all()
            if appointments:
                total_appointments = appointments.count()
                closed_appointments = appointments.filter(appoint_status__in=['Completed', 'Failed', 'Canceled']).count()
                closed_percentage = round((closed_appointments / total_appointments) * 100, 2) if total_appointments > 0 else 0
                appointment_percentage = 100 if total_appointments > 0 else 0
                completed_percentage = round((appointments.filter(appoint_status='Completed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                scheduled_percentage = round((appointments.filter(appoint_status='Scheduled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                canceled_percentage = round((appointments.filter(appoint_status='Canceled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                failed_percentage = round((appointments.filter(appoint_status='Failed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                resolved_percentage = round((appointments.filter(is_resolved=True).count() / total_appointments) * 100, 2) if total_appointments > 0 else 0    

                scheduled_appointments = appointments.filter(appoint_status='Scheduled').count()
                completed_appointments = appointments.filter(appoint_status='Completed').count()
                canceled_appointments = appointments.filter(appoint_status='Canceled').count()
                failed_appointments = appointments.filter(appoint_status='Failed').count()
                resolved_appointments = appointments.filter(is_resolved=True).count()
            else:
                total_appointments = 0
                closed_appointments = 0
                closed_percentage = 0
                appointment_percentage = 0
                completed_percentage = 0
                scheduled_percentage = 0
                canceled_percentage = 0
                failed_percentage = 0
                resolved_percentage = 0

                scheduled_appointments = 0
                completed_appointments = 0
                canceled_appointments = 0
                failed_appointments = 0
                resolved_appointments = 0
            
            return render(request, 'appoint_app/admins_portal.html', {
                'mpesa': mpesa,
                'students_cover': students_cover,
                'medicare': medicare,
                'total_appointments': total_appointments,
                'closed_appointments': closed_appointments,
                'closed_percentage': closed_percentage,
                'scheduled_appointments': scheduled_appointments,
                'completed_appointments': completed_appointments,
                'canceled_appointments': canceled_appointments,
                'failed_appointments': failed_appointments,
                'resolved_appointments': resolved_appointments,
                'appointment_percentage': appointment_percentage,
                'scheduled_percentage': scheduled_percentage,
                'completed_percentage': completed_percentage,
                'canceled_percentage': canceled_percentage,
                'failed_percentage': failed_percentage,
                'resolved_percentage': resolved_percentage
            })
        elif user.is_Staff_Patient:
            payments = Payment.objects.filter(patient=user)
            
            mpesa = payments.count()
            appointments = Appointment.objects.filter(appointee=user)
            if appointments:
                total_appointments = appointments.count()
                closed_appointments = appointments.filter(appoint_status__in=['Completed', 'Failed', 'Canceled']).count()
                closed_percentage = round((closed_appointments / total_appointments) * 100, 2) if total_appointments > 0 else 0
                appointment_percentage = 100 if total_appointments > 0 else 0
                completed_percentage = round((appointments.filter(appoint_status='Completed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                scheduled_percentage = round((appointments.filter(appoint_status='Scheduled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                canceled_percentage = round((appointments.filter(appoint_status='Canceled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                failed_percentage = round((appointments.filter(appoint_status='Failed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                resolved_percentage = round((appointments.filter(is_resolved=True).count() / total_appointments) * 100, 2) if total_appointments > 0 else 0    

                scheduled_appointments = appointments.filter(appoint_status='Scheduled').count()
                completed_appointments = appointments.filter(appoint_status='Completed').count()
                canceled_appointments = appointments.filter(appoint_status='Canceled').count()
                failed_appointments = appointments.filter(appoint_status='Failed').count()
                resolved_appointments = appointments.filter(is_resolved=True).count()
            else:
                total_appointments = 0
                closed_appointments = 0
                closed_percentage = 0
                appointment_percentage = 0
                completed_percentage = 0
                scheduled_percentage = 0
                canceled_percentage = 0
                failed_percentage = 0
                resolved_percentage = 0

                scheduled_appointments = 0
                completed_appointments = 0
                canceled_appointments = 0
                failed_appointments = 0
                resolved_appointments = 0
            
            return render(request, 'appoint_app/staff_patients_portal.html', {
                'mpesa': mpesa,
                'total_appointments': total_appointments,
                'closed_appointments': closed_appointments,
                'closed_percentage': closed_percentage,
                'scheduled_appointments': scheduled_appointments,
                'completed_appointments': completed_appointments,
                'canceled_appointments': canceled_appointments,
                'failed_appointments': failed_appointments,
                'resolved_appointments': resolved_appointments,
                'appointment_percentage': appointment_percentage,
                'scheduled_percentage': scheduled_percentage,
                'completed_percentage': completed_percentage,
                'canceled_percentage': canceled_percentage,
                'failed_percentage': failed_percentage,
                'resolved_percentage': resolved_percentage
            })

        elif user.is_Student_Patient:
            payments = Payment.objects.filter(patient=user)
            
            mpesa = payments.count()
            appointments = Appointment.objects.filter(appointee=user)
            if appointments:
                total_appointments = appointments.count()
                closed_appointments = appointments.filter(appoint_status__in=['Completed', 'Failed', 'Canceled']).count()
                closed_percentage = round((closed_appointments / total_appointments) * 100, 2) if total_appointments > 0 else 0
                appointment_percentage = 100 if total_appointments > 0 else 0
                completed_percentage = round((appointments.filter(appoint_status='Completed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                scheduled_percentage = round((appointments.filter(appoint_status='Scheduled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                canceled_percentage = round((appointments.filter(appoint_status='Canceled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                failed_percentage = round((appointments.filter(appoint_status='Failed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                resolved_percentage = round((appointments.filter(is_resolved=True).count() / total_appointments) * 100, 2) if total_appointments > 0 else 0    

                scheduled_appointments = appointments.filter(appoint_status='Scheduled').count()
                completed_appointments = appointments.filter(appoint_status='Completed').count()
                canceled_appointments = appointments.filter(appoint_status='Canceled').count()
                failed_appointments = appointments.filter(appoint_status='Failed').count()
                resolved_appointments = appointments.filter(is_resolved=True).count()
            else:
                total_appointments = 0
                closed_appointments = 0
                closed_percentage = 0
                appointment_percentage = 0
                completed_percentage = 0
                scheduled_percentage = 0
                canceled_percentage = 0
                failed_percentage = 0
                resolved_percentage = 0

                scheduled_appointments = 0
                completed_appointments = 0
                canceled_appointments = 0
                failed_appointments = 0
                resolved_appointments = 0
            
            return render(request, 'appoint_app/student_patients_portal.html', {
                'mpesa': mpesa,
                'total_appointments': total_appointments,
                'closed_appointments': closed_appointments,
                'closed_percentage': closed_percentage,
                'scheduled_appointments': scheduled_appointments,
                'completed_appointments': completed_appointments,
                'canceled_appointments': canceled_appointments,
                'failed_appointments': failed_appointments,
                'resolved_appointments': resolved_appointments,
                'appointment_percentage': appointment_percentage,
                'scheduled_percentage': scheduled_percentage,
                'completed_percentage': completed_percentage,
                'canceled_percentage': canceled_percentage,
                'failed_percentage': failed_percentage,
                'resolved_percentage': resolved_percentage
            })
        elif user.is_Doctor:
            appointments = Appointment.objects.filter(appointed_doctor=user)
            if appointments:
                total_appointments = appointments.count()
                closed_appointments = appointments.filter(appoint_status__in=['Completed', 'Failed', 'Canceled']).count()
                closed_percentage = round((closed_appointments / total_appointments) * 100, 2) if total_appointments > 0 else 0
                appointment_percentage = 100 if total_appointments > 0 else 0
                completed_percentage = round((appointments.filter(appoint_status='Completed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                scheduled_percentage = round((appointments.filter(appoint_status='Scheduled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                canceled_percentage = round((appointments.filter(appoint_status='Canceled').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                failed_percentage = round((appointments.filter(appoint_status='Failed').count() / total_appointments) * 100, 2) if total_appointments > 0 else 0
                resolved_percentage = round((appointments.filter(is_resolved=True).count() / total_appointments) * 100, 2) if total_appointments > 0 else 0    

                scheduled_appointments = appointments.filter(appoint_status='Scheduled').count()
                completed_appointments = appointments.filter(appoint_status='Completed').count()
                canceled_appointments = appointments.filter(appoint_status='Canceled').count()
                failed_appointments = appointments.filter(appoint_status='Failed').count()
                resolved_appointments = appointments.filter(is_resolved=True).count()
            else:
                total_appointments = 0
                closed_appointments = 0
                appointment_percentage = 0
                completed_percentage = 0
                closed_percentage = 0
                scheduled_percentage = 0
                canceled_percentage = 0
                failed_percentage = 0
                resolved_percentage = 0

                scheduled_appointments = 0
                completed_appointments = 0
                canceled_appointments = 0
                failed_appointments = 0
                resolved_appointments = 0
            
            return render(request, 'appoint_app/doctors_portal.html', {
                'total_appointments': total_appointments,
                'closed_appointments': closed_appointments,
                'closed_percentage': closed_percentage,
                'scheduled_appointments': scheduled_appointments,
                'completed_appointments': completed_appointments,
                'canceled_appointments': canceled_appointments,
                'failed_appointments': failed_appointments,
                'resolved_appointments': resolved_appointments,
                'appointment_percentage': appointment_percentage,
                'scheduled_percentage': scheduled_percentage,
                'completed_percentage': completed_percentage,
                'canceled_percentage': canceled_percentage,
                'failed_percentage': failed_percentage,
                'resolved_percentage': resolved_percentage
            })
        else:
            return redirect('home')
    else:
        return render(request, "appoint_app/home.html")
    

# Create a home view
def home(request):
    return render(request, "appoint_app/home.html")


# Create a terms & conditions view
def terms(request):
    return render(request, "appoint_app/terms_and_conditions.html")