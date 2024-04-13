from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, RemovalRequest, Comment, StudyGroups
from .forms import PostForm, CommentForm, RemovalRequestForm, StudyGroupForm
from authentication.models import CustomUser

class TestModels(TestCase):

    def test_post_creation(self):
        author = CustomUser.objects.create_user(username='testuser', password='12345')
        post = Post.objects.create(title='Test Post', content='Content for Test Post', author=author)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Content for Test Post')
        self.assertEqual(post.author, author)

    def test_post_slug_creation(self):
        author = CustomUser.objects.create_user(username='testuser', password='12345')
        post = Post.objects.create(title='Test Post with Slug', content='Content for Test Post with Slug', author=author)
        self.assertEqual(post.slug, 'test-post-with-slug')

    def test_removal_request_creation(self):
        author = CustomUser.objects.create_user(username='testuser', password='12345')
        post = Post.objects.create(title='Test Post', content='Content for Test Post', author=author)
        requestor = CustomUser.objects.create_user(username='testrequestor', password='12345')
        removal_request = RemovalRequest.objects.create(post=post, requested_by=requestor, reason='Test Reason')
        self.assertEqual(removal_request.post, post)
        self.assertEqual(removal_request.requested_by, requestor)
        self.assertEqual(removal_request.reason, 'Test Reason')

    def test_comment_creation(self):
        author = CustomUser.objects.create_user(username='testuser', password='12345')
        post = Post.objects.create(title='Test Post', content='Content for Test Post', author=author)
        commentor = CustomUser.objects.create_user(username='testcommentor', password='12345')
        comment = Comment.objects.create(post=post, name=commentor, email='test@example.com', body='Test Comment')
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.name, commentor)
        self.assertEqual(comment.email, 'test@example.com')
        self.assertEqual(comment.body, 'Test Comment')

    def test_study_group_creation(self):
        author = CustomUser.objects.create_user(username='testuser', password='12345')
        group = StudyGroups.objects.create(title='Test Group', description='Description for Test Group', division='Software Engineering', author=author)
        self.assertEqual(group.title, 'Test Group')
        self.assertEqual(group.description, 'Description for Test Group')
        self.assertEqual(group.division, 'Software Engineering')
        self.assertEqual(group.author, author)

class TestForms(TestCase):

    def test_post_form_valid(self):
        form = PostForm(data={'title': 'Test Post', 'Topic_choice': 'summaries', 'content': 'Content for Test Post', 'department_choices': 'Software Engineering'})
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_removal_request_form_valid(self):
        form = RemovalRequestForm(data={'reason': 'Test Reason'})
        self.assertTrue(form.is_valid())

    def test_removal_request_form_invalid(self):
        form = RemovalRequestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_study_group_form_valid(self):
        form = StudyGroupForm(data={'title': 'Test Group', 'description': 'Description for Test Group', 'division': 'Software Engineering', 'group_size': 5})
        self.assertTrue(form.is_valid())

    def test_study_group_form_invalid(self):
        form = StudyGroupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.post1 = Post.objects.create(title='Test Post 1', content='Content for Test Post 1')
        self.post2 = Post.objects.create(title='Test Post 2', content='Content for Test Post 2')

    def test_PostList_GET(self):
        response = self.client.get(reverse('homeBlog'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Forum.html')

    def test_PostDetail_GET(self):
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post1.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'Post.html')

    def test_AddPostView_GET(self):
        response = self.client.get(reverse('add_post'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'question_page.html')

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import (
    PostList,
    post_detail,
    AddPostView,
    UpdatePostView,
    remove_post,
    add_post_benefits,
    editorspost,
    request_removal,
    request_removal_benefits,
    Study_groups,
    join_group,
    create_group,
    remove_group,
    add_post_rights,
    benefits_view,
    reserve_view,
    add_post_reserve,
    allevents,
    allWorkshops,
    allScholarships,
)

class TestUrls(SimpleTestCase):

    def test_homeBlog_url_resolved(self):
        url = reverse('homeBlog')
        self.assertEquals(resolve(url).func.view_class, PostList)

    def test_post_detail_url_resolved(self):
        url = reverse('post_detail')
        self.assertEquals(resolve(url).func, post_detail)

    def test_update_post_url_resolved(self):
        url = reverse('update_post', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, UpdatePostView)

    def test_remove_post_url_resolved(self):
        url = reverse('remove_post', args=[1])
        self.assertEquals(resolve(url).func, remove_post)

    def test_add_post_benefits_url_resolved(self):
        url = reverse('Add_benefits')
        self.assertEquals(resolve(url).func, add_post_benefits)

    def test_editorspost_url_resolved(self):
        url = reverse('studentrights')
        self.assertEquals(resolve(url).func, editorspost)

    def test_request_removal_url_resolved(self):
        url = reverse('request_removal', args=[1])
        self.assertEquals(resolve(url).func, request_removal)

    def test_request_removal_benefits_url_resolved(self):
        url = reverse('request_removal_benefits', args=[1])
        self.assertEquals(resolve(url).func, request_removal_benefits)

    def test_study_groups_url_resolved(self):
        url = reverse('study_groups')
        self.assertEquals(resolve(url).func, Study_groups)

    def test_join_group_url_resolved(self):
        url = reverse('join_group', args=[1])
        self.assertEquals(resolve(url).func, join_group)

    def test_create_group_url_resolved(self):
        url = reverse('create_group')
        self.assertEquals(resolve(url).func, create_group)

    def test_remove_group_url_resolved(self):
        url = reverse('delete_group', args=[1])
        self.assertEquals(resolve(url).func, remove_group)

    def test_add_post_rights_url_resolved(self):
        url = reverse('Add_right')
        self.assertEquals(resolve(url).func, add_post_rights)

    def test_benefits_view_url_resolved(self):
        url = reverse('studentbenefits')
        self.assertEquals(resolve(url).func, benefits_view)

    def test_reserve_view_url_resolved(self):
        url = reverse('reserve')
        self.assertEquals(resolve(url).func, reserve_view)

    def test_add_post_reserve_url_resolved(self):
        url = reverse('Add_reserve')
        self.assertEquals(resolve(url).func, add_post_reserve)

    def test_allevents_url_resolved(self):
        url = reverse('Events')
        self.assertEquals(resolve(url).func, allevents)

    def test_allWorkshops_url_resolved(self):
        url = reverse('Workshops')
        self.assertEquals(resolve(url).func, allWorkshops)

    def test_allScholarships_url_resolved(self):
        url = reverse('Scholarships')
        self.assertEquals(resolve(url).func, allScholarships)
