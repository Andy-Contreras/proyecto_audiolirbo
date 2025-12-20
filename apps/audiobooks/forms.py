from django import forms
from .models import Audiobook, Questions, AnswerOption, Vocabulario
from django.forms import inlineformset_factory
from django.contrib.auth.forms import PasswordChangeForm
class AudiobookForm(forms.ModelForm):
    class Meta:
        model = Audiobook
        fields = ['title', 'author_name', 'audio_file', 'cover_image']
        widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Ej: El Principito'}),
        'author_name': forms.TextInput(attrs={'placeholder': 'Autor'}),
        }

class VocabularioForm(forms.ModelForm):
    class Meta:
        model = Vocabulario
        fields = ["palabra", "definicion", "ejemplo"]
        widgets = {
            "palabra": forms.TextInput(attrs={"class": "form-control"}),
            "definicion": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "ejemplo": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }


# VocabularioFormSet = inlineformset_factory(
#     Audiobook,
#     Vocabulario,
#     form=VocabularioForm,
#     extra=1,
#     can_delete=True
# )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Ingresa tu contraseña actual"
        })
    )

    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Nueva contraseña"
        })
    )

    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Repite la nueva contraseña"
        })
    )