from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#blogs
STATUS=( #Status of the blog post.
    (0,"draft"), # making  a draft of the user.
    (1,"Publish")#published
)

def validate_file_extension(value):#making sure we can upload a file.
    import os
    from django.conf import settings
    ext = os.path.splitext(value.name)[1]  # Get file extension
    valid_extensions = ['.png', '.pdf', '.docx']  
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Only pdf,png and docx are allowed'))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True) #unique is an valiation to check if max length is not greater.
    slug = models.SlugField(max_length=200, unique=True)#checks that it gets only string,chars,numbers
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')#
    updated_on = models.DateTimeField(auto_now= True)#model to update the date of an update.
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)#checks if the blog is publish or draft.
    header_image = models.FileField(null=True,blank =True,upload_to="images/",validators=[validate_file_extension])#images.
    

    class Meta:
        ordering = ['-created_on']#See when the blog was posted.

    # def __str__(self) -> str:
    #     return self.title#return the title of the blog.
    def get_absolute_url(self):
        return reverse('homeBlog')
#comments.
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)