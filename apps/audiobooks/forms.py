from django import forms
from .models import Audiobook, Questions, AnswerOption, Vocabulario
from django.forms import inlineformset_factory
from django.contrib.auth.forms import PasswordChangeForm
import os
class AudiobookForm(forms.ModelForm):
    class Meta:
        model = Audiobook
        fields = ['title', 'author_name', 'audio_file', 'cover_image','pdf_file']
        widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Ej: El Principito'}),
        'author_name': forms.TextInput(attrs={'placeholder': 'Autor'}),
        'audio_file': forms.FileInput(), 
        'cover_image': forms.FileInput(), 
        'pdf_file': forms.FileInput(),  
        }
    # Validar audio/video
    # Validar audio / video
    def clean_audio_file(self):
        audio = self.cleaned_data.get('audio_file')

        # 🔹 Si es creación (no hay instancia aún)
        if not audio and not self.instance.pk:
            raise forms.ValidationError(
                "El archivo de audio o video es obligatorio."
            )

        if audio:
            max_size = 100 * 1024 * 1024  # 🔥 100 MB recomendado
            if audio.size > max_size:
                raise forms.ValidationError(
                    "El archivo no puede superar los 100 MB."
                )

            ext = os.path.splitext(audio.name)[1].lower()
            allowed_audio = ['.mp3', '.wav', '.ogg']
            allowed_video = ['.mp4', '.webm']

            if ext not in allowed_audio + allowed_video:
                raise forms.ValidationError(
                    "Formato no permitido (mp3, wav, ogg, mp4, webm)."
                )

        return audio

    # Validar imagen
    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')

        if image:
            max_size = 5 * 1024 * 1024  # 5 MB
            if image.size > max_size:
                raise forms.ValidationError(
                    "La imagen no puede superar los 5 MB."
                )

            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                raise forms.ValidationError(
                    "Formato de imagen no válido."
                )

        return image

    # Validar PDF
    def clean_pdf_file(self):
        pdf = self.cleaned_data.get('pdf_file')

        if pdf:
            max_size = 10 * 1024 * 1024  # 10 MB
            if pdf.size > max_size:
                raise forms.ValidationError(
                    "El PDF no puede superar los 10 MB."
                )

            if not pdf.name.lower().endswith('.pdf'):
                raise forms.ValidationError(
                    "El archivo debe ser un PDF."
                )

        return pdf

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