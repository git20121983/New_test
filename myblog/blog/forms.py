from django import forms
from .models import Comment



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'inp', 'placeholder': 'NAME'}) )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'inp', 'placeholder': 'Your Name'}))
    to = forms.EmailField( widget=forms.TextInput(attrs={'class': 'inp', 'placeholder': 'E-MAIL'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'inp', 'placeholder': 'TEXT E-mail'}))
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']  