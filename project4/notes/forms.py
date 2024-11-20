from django import forms
from .models import Comment

class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name','text')

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前',max_length=50)
    email = forms.EmailField(label='メールアドレス')
    message = forms.CharField(widget=forms.Textarea,label='メッセージ')