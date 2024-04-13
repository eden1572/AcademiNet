from django.db import models
from django.utils import timezone

from django.urls import reverse 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from authentication.models import CustomUser
from django.contrib.auth import get_user_model
from authentication.forms import SigninForm
#blogs
STATUS=( #Status of the blog post.
    (0,"draft"), # making  a draft of the user.
    (1,"Publish")#published
)
User = get_user_model

department_choice =  [
        ('Software Engineering', 'Software Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Architecture', 'Architecture'),
        ('Structural Engineering', 'Structural Engineering'),
        ('Industrial Engineering', 'Industrial Engineering'),
        ('Computer science', 'Computer science'),
        ('Chemical Engineering','Chemical Engineering'),
    ]
Topic_choice = [
    ('summaries','Summaries'),
    ('Help with the educational material','Help with the educational material'),
    ('Study Groups','Study Groups'),
]

rights_benefits_choice = [
    ('Exams','Exams'),
    ('Reserve','Reserve'),
    ('Events','Events')

]#need to change name to rights onlyy...

benefits_choice = [
    ('Events','Events'),
    ('workshops','workshops'),
    ('Scholarships','Scholarships'),#change to schoolships

]

reserve_choices = [
    ('Preferred rights','Preferred rights'),
    ('Protection from dismissal','Protection from dismissal'),
    ('rates','rates'),

]


def validate_file_extension(value):#making sure we can upload a file.
    import os
    from django.conf import settings
    valid_extensions = ['.png', '.pdf', '.docx']  
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Only pdf,png and docx are allowed'))
     
def sizefile(self):
     limit = 1073741824 #size under 1gb.
     if self.size > limit:
         raise ValidationError('File too big, max size is 1gb per file.')
     
def title_exists(title):
    # Perform a query to check if a post with the given title exists
    return Post.objects.filter(title=title).exists()

CustomUser = get_user_model()

class Post(models.Model):   
    
    title = models.CharField(max_length=200, unique=True) #unique is an valiation to check if max length is not greater.
    slug = models.SlugField(max_length=200, unique=True,null=True)#checks that it gets only string,chars,numbers, DELETE!
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True)
    isanonymous = models.BooleanField(default=False)#giving the option to make a anonymous sumbit
    Topic_choice = models.CharField(max_length=100,choices=Topic_choice,null=True)
    benefits_rights_choices = models.CharField(max_length=100,choices=rights_benefits_choice,null=True)
    benefits_choices = models.CharField(max_length=100,choices=benefits_choice,null=True)#for benefits page.
    reserve_choices = models.CharField(max_length=100,choices=reserve_choices,null=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author_url  = models.URLField(blank=True, null=True)
    isright = models.BooleanField(default=False)#rights posts.
    isbenefits = models.BooleanField(default=False)#for events posts
    isreserve = models.BooleanField(default=False)#for reserve(soilders_posts)posts
    header_image = models.FileField(null=True,blank =True,upload_to="images/",validators=[validate_file_extension,sizefile])#images.
    department_choices = models.CharField(max_length = 200, choices = department_choice,default = 'tech')
    
    def save(self,current_user=None, *args, **kwargs):#saving post
         # Generate slug from title
          self.slug = slugify(self.title)
          super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_on']#See when the blog was posted.

    def get_absolute_url(self):
        return reverse('homeBlog')
    
    
User = get_user_model()

class RemovalRequest(models.Model):#remove option
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    is_approved = models.BooleanField(default=False)
    
   
   
#comments.
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    #name = models.CharField(max_length=80)
    name = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    file_comment_upload = models.FileField(null=True,blank=True,upload_to="images/",validators=[validate_file_extension,sizefile])
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    
#Study Groups
class StudyGroups(models.Model):#making  groups
    title = models.CharField(max_length = 100,unique=True)#so there won't be same groups.
    description  = models.TextField()
    division = models.CharField(max_length=100,choices=department_choice)
    data_created = models.DateTimeField(auto_now_add=True)
    group_size = models.IntegerField(default=3)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True)#shows the group author.

    def get_users(self):
        # Retrieve all users belonging to this group using GroupMembers
        return self.groupmembers_set.all()

class GroupMembers(models.Model):#making a way to users to join one
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroups,on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    left_date = models.DateTimeField(null=True,blank=True)

    def leave_group(self):
        self.left_date = timezone.now()
        self.save()#for current user.

