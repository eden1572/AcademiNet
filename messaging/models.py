from django.db import models
from django.contrib.auth import get_user_model
from blog.models import validate_file_extension,sizefile
from authentication.models import CustomUser
#from authentication.models import CustomUser

title_choice = [
    ('User Error','User Error'),
    ('Forum Problem','Forum Problem'),
    ('Rights and Benefits','Rights and Benefits'),
    ('Other','Other'),
]

User = get_user_model()
class Message(models.Model):#sendig messages to admin about issues in the web
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name="sent_messages",null=True)
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    problem_solved = models.BooleanField(default=False)#option to see if problem was solved.
    file_sumbit_upload = models.FileField(null=True,blank=True,upload_to="images/",validators=[validate_file_extension,sizefile])
    title_message =  models.CharField(max_length=100,choices=title_choice,null=True)
    issue = models.BooleanField(default=False)#making a type of msg that will be as errors, False = not msg about issue.
    
class Notification(models.Model):#notifications.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    