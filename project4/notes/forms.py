from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True, label='メールアドレス')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name','text')

class ContactForm(forms.Form):
    name = forms.CharField(
        label='お名前',
        max_length=50,
        required=True
        )
    company = forms.CharField(
        label='会社名',
        required=False
    )
    email = forms.EmailField(
        label='メールアドレス',
        required=True
        )
    message = forms.CharField(
        widget=forms.Textarea,
        label='メッセージ',
        max_length=1000,
        required=True
        )
