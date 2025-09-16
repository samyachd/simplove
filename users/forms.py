from django import forms
from django.contrib.auth.models import User
from .models import UserAccount


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error(
                "confirm_password", "Les mots de passe ne correspondent pas."
            )
        return cleaned_data


class AccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "birth_date",
            "language",
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "phone_number": "Téléphone",
            "address": "Adresse",
            "birth_date": "Date de naissance",
            "language": "Langue",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "language": forms.Select(attrs={"class": "form-select"}),
        }
