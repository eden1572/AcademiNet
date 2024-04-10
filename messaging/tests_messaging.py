from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Message, Notification
from .views import message_list, message_detail, create_message, all_users_notifactions, solve_problem

class InboxURLsTestCase(TestCase):
    def setUp(self):
        self.message = Message.objects.create(subject='Test Message', body='Test Body')
        self.notification = Notification.objects.create(message='Test Notification')

    def test_message_list_url(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')

    def test_message_detail_url(self):
        response = self.client.get(reverse('inbox_post2', args=[self.message.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox_post2.html')

    def test_create_message_url(self):
        response = self.client.get(reverse('create_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_message.html')

    def test_all_users_notifications_url(self):
        response = self.client.get(reverse('notifations_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifactions_list.html')

    def test_solve_problem_url(self):
        response = self.client.get(reverse('solve_problem', args=[self.message.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solve_problem.html')

#froms
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        admin = get_user_model().objects.create_superuser(username='admin', password='adminpassword')
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        Message.objects.create(
            sender=admin,
            receiver=user,
            subject='Test subject',
            body='Test body',
            problem_solved=False,
            title_message='Other',
            issue=True
        )

    def test_sender_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('sender').verbose_name
        self.assertEqual(field_label, 'sender')

    def test_body_max_length(self):
        message = Message.objects.get(id=1)
        max_length = message._meta.get_field('body').max_length
        self.assertEqual(max_length, 200)



class NotificationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')

        Notification.objects.create(
            user=user,
            message='Test message',
            read=False
        )

    def test_user_label(self):
        notification = Notification.objects.get(id=1)
        field_label = notification._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_message_max_length(self):
        notification = Notification.objects.get(id=1)
        max_length = notification._meta.get_field('message').max_length
        self.assertEqual(max_length, 255)

   


#messageing views
from django.test import TestCase, Client
from django.urls import reverse
from .models import Message, Notification
from .forms import MessageForm, SolveProblemForm
from authentication.models import CustomUser, Editor
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class MessageListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 10 messages for testing
        number_of_messages = 10
        admin = CustomUser.objects.create_superuser(username='admin', password='adminpassword')
        for message_id in range(number_of_messages):
            Message.objects.create(
                sender=admin,
                receiver=admin,
                subject=f'Test Subject {message_id}',
                body=f'Test Body {message_id}',
                problem_solved=False,
                title_message='Other',
                issue=True
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/inbox/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')

    def test_lists_all_messages(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['messages']) == 10)

class MessageCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create_message'))
        self.assertRedirects(response, '/accounts/login/?next=/create_message/')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/create_message/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_message'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_message.html')

    def test_create_message(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_message'), {
            'title': 'Test Message Title',
            'Description': 'Test Message Description',
            'divison': 'Other',
            'file': SimpleUploadedFile('test_file.txt', b'test content'),
        })
        self.assertEqual(response.status_code, 302)  # 302 is redirect status code

        # Check if message was created
        self.assertTrue(Message.objects.exists())

    def test_create_message_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_message'), {
            # Missing required fields
            'Description': 'Test Message Description',
            'divison': 'Other',
            'file': SimpleUploadedFile('test_file.txt', b'test content'),
        })
        self.assertEqual(response.status_code, 400)  # 400 is bad request status code

        # Check if message was not created
        self.assertFalse(Message.objects.exists())

