from django import forms
from .models import Comment , Post,validate_file_extension,sizefile,StudyGroups
from authentication.models import CustomUser
from django.db import models


class PostForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = ('title','Topic_choice','content','header_image','department_choices')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].error_messages['unique'] = "A post with this title already exists"


    def clean_header_image(self):#checks that files are in the right format.
        header_image = self.cleaned_data.get('header_image')
        if header_image:
            if(sizefile(header_image) == True):
                validate_file_extension(header_image)
        return header_image

#Search.
class PostSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

#comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body','file_comment_upload')#going to change name and email because we will have users.


#removing post
class RemovalRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)

#groups 
class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroups
        fields = ['title', 'description', 'division', 'group_size']