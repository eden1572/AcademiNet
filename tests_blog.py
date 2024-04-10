from django.test import TestCase
import unittest
from blog.models import Post,Comment
from blog.forms import CommentForm
from blog.views import validate_file_extension
from blog.models import ValidationError
from authentication.admin import CustomUserAdmin
# Create your tests here.
class TestPostModel(unittest.TestCase):
    def test_get_absolute_url(self):
        post = Post(title='Sample Post', slug='sample-post')
        expected_url = reverse('homeBlog')
        self.assertEqual(post.get_absolute_url(), expected_url)


class TestCommentModel(TestCase):
    def test_comment_str(self):
        comment = Comment(body='Great post!', name='John Doe')
        expected_str = 'Comment Great post! by John Doe'
        self.assertEqual(str(comment), expected_str)

class TestFileExtensionValidation(unittest.TestCase):
    def test_valid_extensions(self):
        valid_files = ['file.pdf', 'image.png', 'document.docx']
        for filename in valid_files:
            with self.subTest(filename=filename):
                self.assertIsNone(validate_file_extension(filename))

    def test_invalid_extensions(self):
        invalid_files = ['file.txt', 'image.jpg', 'document.xlsx']
        for filename in invalid_files:
            with self.subTest(filename=filename):
                with self.assertRaises(ValidationError):
                    validate_file_extension(filename)

class TestPostOrdering(TestCase):
    def test_post_order(self):
        post1 = Post.objects.create(title='First Post', slug='first-post')
        post2 = Post.objects.create(title='Second Post', slug='second-post')
        post3 = Post.objects.create(title='Third Post', slug='third-post')

        posts = Post.objects.all()
        self.assertEqual(posts[0], post3)
        self.assertEqual(posts[1], post2)
        self.assertEqual(posts[2], post1)

class CommentFormTest(TestCase):

    def test_valid_data(self):
        """
        Test that the form accepts valid data.
        """
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_name(self):
        """
        Test that the form raises a validation error for an empty name.
        """
        data = {
            'name': '',
            'email': 'testuser@example.com',
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])

    def test_invalid_email(self):
        """
        Test that the form raises a validation error for an invalid email address.
        """
        data = {
            'name': 'Test User',
            'email': 'invalid_email',
            'body': 'This is a test comment.'}
        
from django.test import TestCase


#urls.py - templates 
from django.test import TestCase
from django.urls import reverse

class UrlsTestCase(TestCase):
    def test_project_url(self):
        response = self.client.get(reverse('project'))
        self.assertEqual(response.status_code, 200)

    def test_signin_url(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signout_url(self):
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_editor_url(self):
        response = self.client.get(reverse('homepage_editor'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_url(self):
        response = self.client.get(reverse('forgot-password'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_url(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_benefit_rights_url(self):
        response = self.client.get(reverse('benefit_rights'))
        self.assertEqual(response.status_code, 200)

    def test_blog_url(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)

    def test_contact_us_url(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_url(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_url(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_url(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_student_profile_url(self):
        response = self.client.get(reverse('student_profile'))
        self.assertEqual(response.status_code, 200)

    def test_editor_profile_url(self):
        response = self.client.get(reverse('editor_profile'))
        self.assertEqual(response.status_code, 200)

    def test_change_email_student_url(self):
        response = self.client.get(reverse('change-email-student'))
        self.assertEqual(response.status_code, 200)

    def test_change_email_editor_url(self):
        response = self.client.get(reverse('change-email-editor'))
        self.assertEqual(response.status_code, 200)

    def test_change_phone_url(self):
        response = self.client.get(reverse('change-phone'))
        self.assertEqual(response.status_code, 200)


#views.py - templates
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import Editor

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.editor = Editor.objects.create(user=self.user)

    def test_signin(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_signup(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'password', 'password2': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_signout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_signout_admin(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_change_email_student(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('change-email-student'), {'new_email': 'newemail@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_change_email_editor(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('change-email-editor'), {'new_email': 'newemail@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_change_phone(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('change-phone'), {'new_phone': '123456789'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])


#admin.py - Blog
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from blog.admin import PostAdmin, CommentAdmin, StudyGroupsadmin, GroupMembersadmin
from blog.models import Post, Comment, StudyGroups, GroupMembers
from messaging.models import Message

class PostAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.post_admin = PostAdmin(Post, self.site)
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test Content')

    def test_list_display(self):
        self.assertEqual(self.post_admin.list_display, ('title', 'content', 'header_image', 'department_choices'))

    def test_search_fields(self):
        self.assertEqual(self.post_admin.search_fields, ['title', 'content'])


class CommentAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.comment_admin = CommentAdmin(Comment, self.site)
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test Content')
        self.comment = Comment.objects.create(post=self.post, name='Test Commenter', email='test@example.com', body='Test Comment')

    def test_list_display(self):
        self.assertEqual(self.comment_admin.list_display, ('name', 'body', 'post', 'created_on', 'active'))

    def test_list_filter(self):
        self.assertEqual(self.comment_admin.list_filter, ('active', 'created_on'))

    def test_search_fields(self):
        self.assertEqual(self.comment_admin.search_fields, ('name', 'email', 'body'))


class StudyGroupsAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.study_groups_admin = StudyGroupsadmin(StudyGroups, self.site)
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.study_group = StudyGroups.objects.create(author=self.user, title='Test Group', description='Test Description', division='Test Division', group_size=10)

    def test_list_display(self):
        self.assertEqual(self.study_groups_admin.list_display, ('title', 'description', 'division', 'data_created', 'group_size', 'author'))

    def test_list_filter(self):
        self.assertEqual(self.study_groups_admin.list_filter, ('division', 'group_size'))

    def test_search_fields(self):
        self.assertEqual(self.study_groups_admin.search_fields, ['title', 'author'])


class GroupMembersAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.group_members_admin = GroupMembersadmin(GroupMembers, self.site)
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.study_group = StudyGroups.objects.create(author=self.user, title='Test Group', description='Test Description', division='Test Division', group_size=10)
        self.group_member = GroupMembers.objects.create(user=self.user, group=self.study_group)

    def test_list_display(self):
        self.assertEqual(self.group_members_admin.list_display, ('user', 'Group_name', 'join_date', 'left_date'))

    def test_list_filter(self):
        self.assertEqual(self.group_members_admin.list_filter, ('group',))

    def test_ordering(self):
        self.assertEqual(self.group_members_admin.ordering, ['join_date'])

    def test_Group_name(self):
        self.assertEqual(self.group_members_admin.Group_name(self.group_member), 'Test Group')


#forms.py - Blog
from django.test import TestCase
from blog.forms import PostForm, PostSearchForm, CommentForm, RemovalRequestForm, StudyGroupForm
from blog.models import Post, Comment, StudyGroups
from django.core.files.uploadedfile import SimpleUploadedFile

class PostFormTest(TestCase):
    def test_valid_post_form(self):
        form_data = {'title': 'Test Post', 'Topic_choice': 'Test Topic', 'content': 'Test Content'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form_data = {'title': '', 'Topic_choice': 'Test Topic', 'content': 'Test Content'}  # Title is required
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_clean_header_image(self):
        image = SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg')
        form = PostForm()
        form.cleaned_data = {'header_image': image}
        self.assertEqual(form.clean_header_image(), image)

    
class PostSearchFormTest(TestCase):
    def test_valid_post_search_form(self):
        form_data = {'query': 'Test Query'}
        form = PostSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_post_search_form(self):
        form_data = {'query': ''}
        form = PostSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

   
class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form_data = {'body': 'Test Comment Body'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form_data = {'body': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())



class RemovalRequestFormTest(TestCase):
    def test_valid_removal_request_form(self):
        form_data = {'reason': 'Test Removal Reason'}
        form = RemovalRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_removal_request_form(self):
        form_data = {'reason': ''}
        form = RemovalRequestForm(data=form_data)
        self.assertFalse(form.is_valid())

  

class StudyGroupFormTest(TestCase):
    def test_valid_study_group_form(self):
        form_data = {'title': 'Test Group', 'description': 'Test Description', 'division': 'Test Division', 'group_size': 10}
        form = StudyGroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_study_group_form(self):
        form_data = {'title': '', 'description': 'Test Description', 'division': 'Test Division', 'group_size': 10}
        form = StudyGroupForm(data=form_data)
        self.assertFalse(form.is_valid())

   
#test views.messages
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from messaging.models import Message, Notification

class InboxViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')
        self.client.login(username='test_user', password='password')

    def test_message_list_view(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')

    def test_message_detail_view(self):
        message = Message.objects.create(sender=self.user, receiver=self.admin, subject='Test', body='Test message')
        response = self.client.get(reverse('message_detail', args=[message.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox_post2.html')
        self.assertEqual(response.context['message'], message)

    def test_create_message_view(self):
        response = self.client.get(reverse('create_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_message.html')

        # Test message creation
        response = self.client.post(reverse('create_message'), {
            'title': 'Test Title',
            'Description': 'Test Description',
            'division': 'Test Division'
        })
        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertTrue(Message.objects.filter(subject='Test Title').exists())

    def test_solve_problem_view(self):
        message = Message.objects.create(sender=self.user, receiver=self.admin, subject='Test', body='Test message')
        response = self.client.get(reverse('solve_problem', args=[message.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'solve_problem.html')

        # Test solving the problem
        response = self.client.post(reverse('solve_problem', args=[message.pk]), {
            'problem_solved': True
        })
        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertTrue(Message.objects.get(pk=message.pk).problem_solved)
        self.assertTrue(Message.objects.filter(sender=self.admin, receiver=self.user, subject='Your problem has been solved').exists())

    def test_mark_notification_as_read_view(self):
        notification = Notification.objects.create(user=self.user, message='Test Notification')
        response = self.client.post(reverse('mark_notification_as_read'), {
            'notifications': [notification.pk]
        })
        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertTrue(Notification.objects.get(pk=notification.pk).read)

    def test_user_notifications_view(self):
        notification = Notification.objects.create(user=self.user, message='Test Notification')
        response = self.client.get(reverse('user_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifactions_list.html')
        self.assertIn(notification, response.context['notifications'])

    def test_all_users_notifications_view(self):
        notification = Notification.objects.create(user=self.user, message='Test Notification')
        response = self.client.get(reverse('all_users_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifactions_list.html')
        self.assertIn(notification, response.context['notifications'])

