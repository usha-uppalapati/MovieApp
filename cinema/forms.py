from django import forms
from . import models


class SignupForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(max_length=10)
    confirmpassword = forms.CharField(max_length=10)


class SigninForm(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(max_length=10)


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=100, label='comment')
    rating = forms.IntegerField(label='rating')


class PosterForm(forms.ModelForm):
    class Meta:
        model = models.poster
        fields = ['image', 'title']


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.order
        fields = ['movie_id', 'movie_title']


class ForgotPasswordForm(forms.Form):
    name = forms.CharField(max_length=20)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=20)