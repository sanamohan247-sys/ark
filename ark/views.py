from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee

def home_view(request):
    return render (request, 'index.html')

def staff_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('hrms_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('hrms_dashboard')
        else:
            messages.error(request, "Invalid credentials or unauthorized staff access.")

    return render(request, 'Staff_login.html')

def hr_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('hrms_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('hrms_dashboard')
        else:
            messages.error(request, "Invalid credentials or unauthorized HR/Admin access.")

    return render(request, 'hr_login.html')

@login_required
def hrms_dashboard_view(request):
    if not request.user.is_staff:
        return redirect('staff_login')
    
    employees = Employee.objects.all()
    total_employees = employees.count()
    active_employees = employees.filter(is_active=True).count()
    inactive_employees = employees.filter(is_active=False).count()
    
    context = {
        'employees': employees,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
    }
    return render(request, 'hrms_dashboard.html', context)

# Add Employee
@login_required
def add_employee_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access. Only HR/Admin can add employees.")
        return redirect('hrms_dashboard')

    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'on'
        Employee.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            designation=request.POST.get('designation'),
            department=request.POST.get('department'),
            is_active=is_active,
        )
        return redirect('hrms_dashboard')

    return render(request, 'add_employee.html')

# Edit Employee
@login_required
def edit_employee_view(request, emp_id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access. Only HR/Admin can edit employees.")
        return redirect('hrms_dashboard')

    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.designation = request.POST.get('designation')
        employee.department = request.POST.get('department')
        employee.is_active = request.POST.get('is_active') == 'on'
        employee.save()
        return redirect('hrms_dashboard')

    return render(request, 'edit_employee.html', {'employee': employee})

# Delete Employee
@login_required
def delete_employee_view(request, emp_id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access. Only HR/Admin can delete employees.")
        return redirect('hrms_dashboard')

    employee = get_object_or_404(Employee, id=emp_id)
    employee.delete()
    return redirect('hrms_dashboard')

# Toggle Employee Status
@login_required
def toggle_employee_status_view(request, emp_id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access. Only HR/Admin can change employee status.")
        return redirect('hrms_dashboard')

    employee = get_object_or_404(Employee, id=emp_id)
    employee.is_active = not employee.is_active
    employee.save()
    status_str = "Active" if employee.is_active else "Inactive"
    messages.success(request, f"Employee {employee.first_name} {employee.last_name} is now {status_str}.")
    return redirect('hrms_dashboard')

# View Employee (Read-Only)
@login_required
def view_employee_view(request, emp_id):
    if not request.user.is_staff:
        return redirect('staff_login')
    
    employee = get_object_or_404(Employee, id=emp_id)
    return render(request, 'view_employee.html', {'employee': employee})

# Logout Staff
def staff_logout_view(request):
    logout(request)
    return redirect('home')