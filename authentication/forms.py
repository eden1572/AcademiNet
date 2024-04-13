# FORMS
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError #מודל שמשמש לטיפול בשגיאות בפרוייקט 
from .models import CustomUser, Editor
import re 
from django.contrib.auth.hashers import check_password
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model


#טופס הרשמה למשתמשים חדשים
class SignupForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['profile_picture', 'username', 'email', 'password1', 'password2', 'academic_institution', 'department', 'year']

    def clean_profile_picture(self): #בדיקת תקינות שדה תמונת הפרופיל
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture and profile_picture.size > 3145728:
            raise ValidationError("The file is too large. Size should not exceed 3MB.") 
        return profile_picture

#טופס התחברות למשתמשים קיימים במערכת
class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self): #פונקציה המחזירה מילון של נתונים נקיים...מבצעת אימות לנתונים בטופס 
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = CustomUser.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError("Incorrect username or password")

        if not check_password(password, user.password):
            raise forms.ValidationError("Incorrect username or password")

        return cleaned_data

#טופס הרשמה למשתמשי EDITOR - הגשת בקשה באתר להיות עורך. 
#הטופס מתקבל בממשק אדמין. ה-ADMIN יוצר קשר עם המועמד ובהתאם יפתח/לא יפתח חשבון. 
class EditorSignupForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ['full_name', 'phone', 'organization_name', 'role_in_organization']

#טופס לשינוי מייל 
class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(label='New Email')

    def clean_new_email(self): #אימות לנתונים בטופס 
        new_email = self.cleaned_data['new_email']
        if CustomUser.objects.filter(email=new_email).exists():
            raise forms.ValidationError("This email is already in use.")
        return new_email

#טופס לשינוי מספר טלפון
class PhoneChangeForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ['phone']


