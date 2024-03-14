<<<<<<< Updated upstream
from django import forms
from .models import Comment , Post,validate_file_extension

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content','header_image')
    def clean_header_image(self):
        header_image = self.cleaned_data.get('header_image')
        if header_image:
            validate_file_extension(header_image)
        return header_image
#comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')#going to change name and email because we will have users.

#files
=======
from django import forms
from .models import Comment , Post,validate_file_extension

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content','header_image','department_choices')
    def clean_header_image(self):
        header_image = self.cleaned_data.get('header_image')
        if header_image:
            validate_file_extension(header_image)
        return header_image
    
#comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')#going to change name and email because we will have users.

#files
>>>>>>> Stashed changes
