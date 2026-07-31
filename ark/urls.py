from .views import home_view, staff_login_view, staff_logout_view, hrms_dashboard_view, add_employee_view, edit_employee_view, delete_employee_view 
from django.urls import path
from django.contrib import admin
urlpatterns = [
    path('',home_view,name='home'),
   # path('admin\', admin.site.bind),
   path('staff/login/', staff_login_view, name='staff_login'),
   path('staff/logout/', staff_logout_view, name='staff_logout'),
    path('hrms/dashboard/', hrms_dashboard_view, name='hrms_dashboard'),
    path('hrms/employee/add/', add_employee_view, name='add_employee'),
    path('hrms/employee/edit/<int:emp_id>/', edit_employee_view, name='edit_employee'),
    path('hrms/employee/delete/<int:emp_id>/', delete_employee_view, name='delete_employee'),
]
