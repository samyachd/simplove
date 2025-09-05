from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self):
        if User.check_password(password, request.user.password):
            # You can authenticate