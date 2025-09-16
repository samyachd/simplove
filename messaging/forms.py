from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {"content":""}
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',  # classes CSS (Bootstrap etc.)
                    'rows': 5,               # hauteur (nombre de lignes)
                    'cols': 40,              # largeur (nombre de colonnes)
                    'placeholder': 'Écris ton message…',
                    'style': 'resize: none;',  # désactiver le redimensionnement
                }
            ),
        }