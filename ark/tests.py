from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Employee

class HRMSTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a superuser (HR/Admin) for adding/editing/deleting/toggling
        self.admin_user = User.objects.create_superuser(
            username='testadmin',
            email='admin@test.com',
            password='testpassword123'
        )
        # Create a regular staff user for dashboard viewing only
        self.staff_user = User.objects.create_user(
            username='teststaff',
            email='staff@test.com',
            password='testpassword123',
            is_staff=True
        )
        # Create a non-staff user for unauthorized checking
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='testpassword123',
            is_staff=False
        )
        # Create an initial employee
        self.employee = Employee.objects.create(
            first_name='Satya',
            last_name='Narayana',
            email='satya@test.com',
            phone='1234567890',
            designation='Agronomist',
            department='Crop Science'
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_renders(self):
        response = self.client.get(reverse('staff_login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_unauthenticated_redirects(self):
        response = self.client.get(reverse('hrms_dashboard'))
        # Should redirect to login page because login_required
        self.assertEqual(response.status_code, 302)

    def test_dashboard_regular_user_redirects(self):
        self.client.login(username='regular', password='testpassword123')
        response = self.client.get(reverse('hrms_dashboard'))
        self.assertRedirects(response, reverse('staff_login'))

    def test_dashboard_staff_user_access(self):
        self.client.login(username='teststaff', password='testpassword123')
        response = self.client.get(reverse('hrms_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'HRMS Dashboard')
        self.assertContains(response, 'Satya Narayana')

    def test_add_employee(self):
        self.client.login(username='testadmin', password='testpassword123')
        
        # Test GET request
        response = self.client.get(reverse('add_employee'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Employee')
        
        # Test POST request to add employee
        post_data = {
            'first_name': 'Srinu',
            'last_name': 'Rao',
            'email': 'srinu@test.com',
            'phone': '9876543210',
            'designation': 'Drone Pilot',
            'department': 'Operations',
            'is_active': 'on'
        }
        response = self.client.post(reverse('add_employee'), post_data)
        # Should redirect back to dashboard
        self.assertRedirects(response, reverse('hrms_dashboard'))
        
        # Verify db entry
        self.assertTrue(Employee.objects.filter(email='srinu@test.com').exists())

    def test_edit_employee(self):
        self.client.login(username='testadmin', password='testpassword123')
        
        # Test GET request
        response = self.client.get(reverse('edit_employee', args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Employee')
        self.assertContains(response, 'Satya')

        # Test POST request to modify employee
        post_data = {
            'first_name': 'Satyadev',
            'last_name': 'Narayana',
            'email': 'satya.new@test.com',
            'phone': '1112223333',
            'designation': 'Senior Agronomist',
            'department': 'Crop Science',
            'is_active': 'on'
        }
        response = self.client.post(reverse('edit_employee', args=[self.employee.id]), post_data)
        self.assertRedirects(response, reverse('hrms_dashboard'))
        
        # Verify db change
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Satyadev')
        self.assertEqual(self.employee.email, 'satya.new@test.com')

    def test_delete_employee(self):
        self.client.login(username='testadmin', password='testpassword123')
        
        response = self.client.post(reverse('delete_employee', args=[self.employee.id]))
        self.assertRedirects(response, reverse('hrms_dashboard'))
        
        # Verify employee is deleted
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

    def test_logout_view(self):
        self.client.login(username='teststaff', password='testpassword123')
        # Check that we are logged in
        response = self.client.get(reverse('hrms_dashboard'))
        self.assertEqual(response.status_code, 200)

        # Trigger logout
        response = self.client.get(reverse('staff_logout'))
        # Should redirect to home page
        self.assertRedirects(response, reverse('home'))

        # Check that we are no longer logged in (accessing dashboard should now redirect us)
        response = self.client.get(reverse('hrms_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_toggle_employee_status(self):
        # 1. Test toggle as regular staff (should fail / redirect)
        self.client.login(username='teststaff', password='testpassword123')
        response = self.client.post(reverse('toggle_employee_status', args=[self.employee.id]))
        self.assertRedirects(response, reverse('hrms_dashboard'))
        self.employee.refresh_from_db()
        self.assertTrue(self.employee.is_active)  # Still active

        # 2. Test toggle as superuser (should succeed)
        self.client.login(username='testadmin', password='testpassword123')
        response = self.client.post(reverse('toggle_employee_status', args=[self.employee.id]))
        self.assertRedirects(response, reverse('hrms_dashboard'))
        self.employee.refresh_from_db()
        self.assertFalse(self.employee.is_active)  # Toggled to inactive

        # 3. Test toggle again (should toggle back to active)
        response = self.client.post(reverse('toggle_employee_status', args=[self.employee.id]))
        self.assertRedirects(response, reverse('hrms_dashboard'))
        self.employee.refresh_from_db()
        self.assertTrue(self.employee.is_active)  # Toggled back to active
