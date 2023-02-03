from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post, User


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


class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-text'}),
            'first_name': forms.TextInput(attrs={'class': 'form-text'}),
            'last_name': forms.TextInput(attrs={'class': 'form-text'}),
            'email': forms.EmailInput(attrs={'class': 'form-text'}),
        }


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user