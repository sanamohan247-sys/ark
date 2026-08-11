from .views import (
    home_view, staff_login_view, staff_logout_view, hr_login_view,
    hrms_dashboard_view, add_employee_view, edit_employee_view, 
    delete_employee_view, view_employee_view, toggle_employee_status_view
)
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('', home_view, name='home'),
    path('staff/login/', staff_login_view, name='staff_login'),
    path('staff/logout/', staff_logout_view, name='staff_logout'),
    path('hr/login/', hr_login_view, name='hr_login'),
    path('hrms/dashboard/', hrms_dashboard_view, name='hrms_dashboard'),
    path('hrms/employee/add/', add_employee_view, name='add_employee'),
    path('hrms/employee/edit/<int:emp_id>/', edit_employee_view, name='edit_employee'),
    path('hrms/employee/delete/<int:emp_id>/', delete_employee_view, name='delete_employee'),
    path('hrms/employee/view/<int:emp_id>/', view_employee_view, name='view_employee'),
    path('hrms/employee/toggle-status/<int:emp_id>/', toggle_employee_status_view, name='toggle_employee_status'),
]
