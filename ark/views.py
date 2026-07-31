from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee

def home_view(request):
    return render (request, 'index.html')

def staff_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
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
@login_required
def hrms_dashboard_view(request):
    if not request.user.is_staff:
        return redirect('staff_login')
    
    employees = Employee.objects.all()
    total_employees = employees.count()
    unique_depts = employees.values_list('department', flat=True).distinct()
    departments_count = len([d for d in unique_depts if d])
    
    context = {
        'employees': employees,
        'total_employees': total_employees,
        'departments_count': departments_count,
    }
    return render(request, 'hrms_dashboard.html', context)

# Add Employee
@login_required
def add_employee_view(request):
    if not request.user.is_staff:
        return redirect('staff_login')

    if request.method == 'POST':
        Employee.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            designation=request.POST.get('designation'),
            department=request.POST.get('department'),
        )
        return redirect('hrms_dashboard')

    return render(request, 'add_employee.html')

# Edit Employee
@login_required
def edit_employee_view(request, emp_id):
    if not request.user.is_staff:
        return redirect('staff_login')

    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.designation = request.POST.get('designation')
        employee.department = request.POST.get('department')
        employee.save()
        return redirect('hrms_dashboard')

    return render(request, 'edit_employee.html', {'employee': employee})

# Delete Employee
@login_required
def delete_employee_view(request, emp_id):
    if not request.user.is_staff:
        return redirect('staff_login')

    employee = get_object_or_404(Employee, id=emp_id)
    employee.delete()
    return redirect('hrms_dashboard')

# Logout Staff
def staff_logout_view(request):
    logout(request)
    return redirect('staff_login')