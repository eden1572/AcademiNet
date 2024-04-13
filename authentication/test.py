# models
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Editor

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_create_user(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.email, 'test@example.com')

    def test_custom_user_str(self):
        self.assertEqual(str(self.user), self.user.username)

class EditorModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='editoruser',
            email='editor@example.com',
            password='editorpass'
        )
        self.editor = Editor.objects.create(
            user=self.user,
            full_name='Test Editor',
            phone='1234567890',
            organization_name='Test Org',
            role_in_organization='Editor'
        )

    def test_create_editor(self):
        self.assertTrue(isinstance(self.editor, Editor))
        self.assertEqual(self.editor.full_name, 'Test Editor')

    def test_editor_user_relationship(self):
        self.assertEqual(self.editor.user, self.user)

# forms
from django.test import TestCase
from .forms import SignupForm

class SignupFormTest(TestCase):
    def test_signup_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'academic_institution': 'Example University',
            'department': 'Computer Science',
            'year': '2022'
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',  # invalid email format
            'password1': 'short',      # password too short
            'password2': 'short',      # password too short
            'academic_institution': 'Example University',
            'department': 'Computer Science',
            'year': '2022'
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

# url test
import unittest
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.urls import urlpatterns
from . import views

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, views.index)

    def test_signin_url_resolves(self):
        url = reverse('signin')
        self.assertEquals(resolve(url).func, views.signIn)

# admin.py -templates
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.sites import AdminSite
from authentication.admin import CustomUserAdmin, EditorAdmin
from authentication.models import CustomUser, Editor
from django.contrib.auth.hashers import make_password

class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.custom_user_admin = CustomUserAdmin(CustomUser, self.site)
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com', last_login=timezone.now(), date_joined=timezone.now(), last_activity=timezone.now())

    def test_is_currently_active(self):
        self.user.last_activity = timezone.now() - timedelta(minutes=3)
        self.assertTrue(self.custom_user_admin.is_currently_active(self.user))
        
        self.user.last_activity = timezone.now() - timedelta(minutes=10)
        self.assertFalse(self.custom_user_admin.is_currently_active(self.user))

    def test_is_active_last_7_days(self):
        self.user.last_activity = timezone.now() - timedelta(days=3)
        self.assertTrue(self.custom_user_admin.is_active_last_7_days(self.user))
        
        self.user.last_activity = timezone.now() - timedelta(days=10)
        self.assertFalse(self.custom_user_admin.is_active_last_7_days(self.user))

# views
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Editor
from .views import signIn, signUp

class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='test_user', email='test@example.com', password='password')
        self.admin = get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        self.editor = Editor.objects.create(user=self.user)

    def test_signIn(self):
        # Test for successful login
        response = self.client.post('/signIn/', {'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertTrue(response.json()['success'])
        
        # Test for incorrect credentials
        response = self.client.post('/signIn/', {'username': 'test_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertFalse(response.json()['success'])

    def test_signUp(self):
        # Test for successful signup
        response = self.client.post('/signUp/', {'username': 'new_user', 'email': 'new@example.com', 'password1': 'new_password', 'password2': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertTrue(response.json()['success'])
        
        # Test for invalid signup (missing fields)
        response = self.client.post('/signUp/', {'username': 'new_user', 'password1': 'new_password', 'password2': 'new_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
        self.assertFalse(response.json()['success'])

    def test_signOut(self):
        response = self.client.get('/signOut/')
        self.assertEqual(response.status_code, 302)  # Should redirect to project page after signout

    def test_signout_admin(self):
        response = self.client.get('/signout_admin/')
        self.assertEqual(response.status_code, 302)  # Should redirect to admin login page after signout

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.client.get('/homepage/')
        self.assertEqual(response.status_code, 200)

# authentication-Models

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import CustomUser, Editor, AdminNotification

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='password')
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password'))

class EditorModelTest(TestCase):
    def test_create_editor(self):
        user = CustomUser.objects.create_user(username='test_user', email='test@example.com', password='password')
        editor = Editor.objects.create(user=user, full_name='John Doe', phone='1234567890', organization_name='ABC Corp', role_in_organization='Manager')
        self.assertEqual(editor.full_name, 'John Doe')
        self.assertEqual(editor.phone, '1234567890')
        self.assertEqual(editor.organization_name, 'ABC Corp')
        self.assertEqual(editor.role_in_organization, 'Manager')

class AdminNotificationModelTest(TestCase):
    def test_create_notification(self):
        notification = AdminNotification.objects.create(message='Test notification', is_treated=False)
        self.assertEqual(notification.message, 'Test notification')
        self.assertFalse(notification.is_treated)

class CustomUserManagerTest(TestCase):
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user(self):
        user = get_user_model().objects.create_user(username='test_user', email='test@example.com', password='password')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

class CustomUserModelAdditionalTests(TestCase):
    def test_user_with_default_values(self):
        # Create a user with only the required fields to check default values
        user = get_user_model().objects.create_user(username='minimaluser', password='testpass123')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.last_activity)  # Assuming default is None if not set

    def test_user_string_representation(self):
        # Verify the string representation of the user is as expected
        user = get_user_model().objects.create_user(username='testuser2', email='test2@example.com', password='testpass123')
        self.assertEqual(str(user), 'testuser2')

    def test_user_email_case_insensitivity(self):
        # Ensure the email field treats "example.com" and "Example.COM" as the same domain
        user1 = get_user_model().objects.create_user(username='user1', email='test@EXAMPLE.com', password='testpass')
        user2 = get_user_model().objects.create_user(username='user2', email='test@example.COM', password='testpass')
        self.assertEqual(user1.email.lower(), user2.email.lower())

class EditorModelAdditionalTests(TestCase):
    def test_editor_without_user(self):
        # Create an editor without linking a user to test handling of null user fields
        editor = Editor.objects.create(full_name='John Editor', phone='1234567890')
        self.assertIsNone(editor.user)
        self.assertFalse(editor.is_approved)

    def test_editor_str_representation(self):
        # Testing the string representation of the Editor
        user = get_user_model().objects.create_user(username='editor1', email='editor1@example.com', password='password123')
        editor = Editor.objects.create(user=user, full_name='Jane Editor', phone='0987654321')
        self.assertEqual(str(editor), 'Jane Editor')


from django.test import TestCase
from .forms import SignupForm, SigninForm, EditorSignupForm, EmailChangeForm, PhoneChangeForm

class FormsTestCase(TestCase):
    def test_signup_form_valid_data(self):
        form = SignupForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'academic_institution': 'Test University',
            'department': 'Test Department',
            'year': '2023'
        })
        self.assertTrue(form.is_valid())

    def test_signin_form_valid_data(self):
        form = SigninForm(data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_editor_signup_form_valid_data(self):
        form = EditorSignupForm(data={
            'full_name': 'Test Editor',
            'phone': '1234567890',
            'organization_name': 'Test Organization',
            'role_in_organization': 'Editor'
        })
        self.assertTrue(form.is_valid())

    def test_email_change_form_valid_data(self):
        form = EmailChangeForm(data={
            'new_email': 'newemail@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_phone_change_form_valid_data(self):
        form = PhoneChangeForm(data={
            'phone': '9876543210'
        })
        self.assertTrue(form.is_valid())

class FormsAdditionalTests(TestCase):
    def test_signup_form_email_normalization(self):
        # Test that the email is normalized to a common format
        form_data = {
            'username': 'newuser',
            'email': 'Test@Example.Com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'academic_institution': 'Example University',
            'department': 'Computer Science',
            'year': '2022'
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'test@example.com')  # Assuming email normalization to lowercase
