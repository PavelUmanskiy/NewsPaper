from django import forms

from .models import *


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = [
            'post_type',
            'categories',
            'title',
            'content',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-text'}),
            'content': forms.Textarea(attrs={'class': 'form-text', 'cols': 100, 'rows': 15}),
        }