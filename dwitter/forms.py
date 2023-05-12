from django import forms
from .models import *


class DweetForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Dweet something...",
                                   "class": "textarea is-success is-medium",
                               }
                           ),
                           label="",)

    class Meta:
        model = Dweet
        exclude = ("user", )


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Username")
    password = forms.CharField(required=True, widget=forms.widgets.PasswordInput, label="Password")
