from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']


class PhotoForm(forms.ModelForm):
    edit_photo = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    class Meta:
        model = models.Photo
        fields = ['image', 'caption']


class DeletePhotoForm(forms.Form):
    delete_photo = forms.BooleanField(widget=forms.HiddenInput(), initial=True)


class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    class Meta:
        model = models.Blog
        fields = ['title', 'content']


class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
