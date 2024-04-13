from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone   
from django.contrib.auth import get_user_model #קבלת מודל המשתמש הנוכחי 

#הגדרת יוזר סטונדט והשדות המשוייכים אליו
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(blank=True)
    academic_institution = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=30, blank=True)
    year = models.CharField(max_length=10, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)
    is_editor = models.BooleanField(default=False)

    def __str__(self): #ייצוג ההדפסה של משתמש סטודנט 
        return self.username

#הגדרת יוזר עורך והשדות המשוייכים אליו 
#מתבצע שימוש במפתח זר למודל המשתמש - כלומר כל משתמש עורך מקושר למשתמש יחיד במערכת 
class Editor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='editor',
        null=True,#מאפשר שדה ריק
        blank=True #מאפשר שדה ריק
    )
    full_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    organization_name = models.CharField(max_length=15)
    role_in_organization = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)

    def __str__(self):  #ייצוג ההדפסה של משתמש עורך 
        return self.full_name

#מנגנון ליצירת התרעות בממשק הניהול של DJANGO
#מגדירים את התכונות והמבנה של המודל
class AdminNotification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    is_treated = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='pictures/', blank=True, null=True)

    def __str__(self):
        return f"Notification (treated: {self.is_treated}) - {self.message[:50]}"


User = get_user_model() #ייבוא מודל המותאם אישית למשתשמש 
