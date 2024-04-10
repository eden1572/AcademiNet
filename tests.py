from django.test import TestCase

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
        self.assertTrue(form.is_valid())

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