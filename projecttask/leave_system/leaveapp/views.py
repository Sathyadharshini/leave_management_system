from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives

import csv

from .models import Leave
from .forms import LeaveForm, RegisterForm, LeaveFilterForm


def home(request):
    return render(request, 'home.html')


def is_manager(user):
    return user.is_staff


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('apply_leave')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            return redirect('my_leaves')
    else:
        form = LeaveForm()
    return render(request, 'apply_leave.html', {'form': form})


@login_required
def my_leaves(request):
    leaves = Leave.objects.filter(employee=request.user)
    return render(request, 'my_leaves.html', {'leaves': leaves})


@login_required
@user_passes_test(is_manager)
def manage_leaves(request):
    form = LeaveFilterForm(request.GET)
    leaves = Leave.objects.all()
    if form.is_valid():
        status = form.cleaned_data['status']
        if status and status != 'All':
            leaves = leaves.filter(status=status)

    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leave_requests.csv"'
        writer = csv.writer(response)
        writer.writerow(['Employee', 'Type', 'Start', 'End', 'Status'])
        for l in leaves:
            writer.writerow([l.employee.username, l.leave_type, l.start_date, l.end_date, l.status])
        return response

    return render(request, 'manage_leaves.html', {'leaves': leaves, 'form': form})


@login_required
@user_passes_test(is_manager)
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if leave.status == 'Pending':
        days = (leave.end_date - leave.start_date).days + 1
        profile = leave.employee.employeeprofile
        if profile.leave_balance >= days:
            profile.leave_balance -= days
            profile.save()
            leave.status = 'Approved'
            leave.save()
            send_status_email(leave)
        else:
            messages.error(request, "Insufficient leave balance.")
    return redirect('manage_leaves')


@login_required
@user_passes_test(is_manager)
def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    if leave.status == 'Pending':
        leave.status = 'Rejected'
        leave.save()
        send_status_email(leave)
    return redirect('manage_leaves')


def send_status_email(leave):
    subject = "Leave Request Status Updated"
    message = f"Hi {leave.employee.username}, your leave from {leave.start_date} to {leave.end_date} was {leave.status}."
    send_mail(
        subject,
        message,
        'admin@example.com',  # change this to your email or use settings.EMAIL_HOST_USER
        [leave.employee.email],
        fail_silently=True
    )


@login_required
@user_passes_test(is_manager)
def dashboard(request):
    total = Leave.objects.count()
    pending = Leave.objects.filter(status='Pending').count()
    approved = Leave.objects.filter(status='Approved').count()
    rejected = Leave.objects.filter(status='Rejected').count()
    return render(request, 'dashboard.html', {
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    })


@login_required
def redirect_after_login(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('apply_leave')


from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

def test_email(request):
    send_mail(
        subject='Test Email',
        message='This is a test email from your localhost Django project!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['yourfriend@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent!")

    



    