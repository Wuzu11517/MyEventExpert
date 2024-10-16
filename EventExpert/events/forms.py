from django import forms
from .models import EmailList

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailList
        fields = ['email']

class MessageForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)