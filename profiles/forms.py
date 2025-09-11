from django import forms
from .models import MemberProfile


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
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
            "age": forms.NumberInput(attrs={"class": "form-control", 'required':True}),
            "location": forms.TextInput(attrs={"class": "form-control", 'required':True}),
        }