from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject','title_message', 'body','file_sumbit_upload']

        file = forms.FileField(required=False)  # Add file input field

class SolveProblemForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['problem_solved']