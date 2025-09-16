from django import forms
from .models import MemberProfile

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = [
            "photo",
            "gender",
            "orientation",
            "age",
            "bio",
            "location",
            "interests",
            "looking_for",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "interest": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            'interests': forms.CheckboxSelectMultiple(attrs={'class': 'my-checkboxes'}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }

        labels = {
            "gender": "Genre",
            "orientation": "Orientation",
            "age": "Âge",
            "bio": "Biographie",
            "location": "Localisation",
            "interests":"Centres d'intérêt",
            "looking_for": "Recherche",
        }


class ProfileFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Nom ou pseudo",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Rechercher..."}
        ),
    )
    age_min = forms.IntegerField(
        required=False,
        label="Âge min",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    age_max = forms.IntegerField(
        required=False,
        label="Âge max",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    gender = forms.ChoiceField(
        required=False,
        label="Genre",
        choices=[("", "Tous")] + MemberProfile.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    orientation = forms.ChoiceField(
        required=False,
        label="Orientation",
        choices=[("", "Toutes")] + MemberProfile.ORIENTATION_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    location = forms.CharField(
        required=False,
        label="Ville",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ex: Paris"}
        ),
    )
    looking_for = forms.ChoiceField(
        required=False,
        label="Recherche",
        choices=[("", "Toutes")] + MemberProfile.LOOKING_FOR_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    interests = forms.CharField(
        required=False,
        label="Intérêts (séparés par des virgules)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ex: sport, musique"}
        ),
    )