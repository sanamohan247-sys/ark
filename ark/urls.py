from .views import home_view
from django.urls import path
from django.contrib import admin
urlpatterns = [
    path('',home_view,name='home'),
   # path('admin\', admin.site.bind),
]