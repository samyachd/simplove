from django import forms
from .models import MemberProfil


class MemberProfilForm(forms.ModelForm):
    class Meta:
        model = MemberProfil
        fields = [
            "gender",
            "orientation",
            "age",
            "bio",
            "location",
            "interest",
            "looking_for",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "interest": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }
