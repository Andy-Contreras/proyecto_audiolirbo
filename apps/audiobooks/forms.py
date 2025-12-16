from django import forms
from .models import Audiobook, Questions, AnswerOption, Vocabulario
from django.forms import inlineformset_factory

class AudiobookForm(forms.ModelForm):
    class Meta:
        model = Audiobook
        fields = ['title', 'author_name', 'audio_file', 'cover_image']
        widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Ej: El Principito'}),
        'author_name': forms.TextInput(attrs={'placeholder': 'Autor'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Escribe la pregunta'
            })
        }

class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = [
            'text',
            'is_correct',
            'justification',
            'points_if_correct',
            'points_if_wrong'
        ]
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Respuesta'}),
            'justification': forms.Textarea(attrs={'rows': 2}),
        }
        def clean(self):
            cleaned_data = super().clean()
            is_correct = cleaned_data.get("is_correct")

            if is_correct and not cleaned_data.get("justification"):
                raise forms.ValidationError(
                    "Debes agregar una justificación para la respuesta correcta."
                )

            return cleaned_data


class VocabularioForm(forms.ModelForm):
    class Meta:
        model = Vocabulario
        fields = ['palabra', 'definicion', 'ejemplo']


QuestionFormSet = inlineformset_factory(
    Audiobook,
    Questions,
    form=QuestionForm,
    extra=1,
    can_delete=True
)
AnswerFormSet = inlineformset_factory(
    Questions,
    AnswerOption,
    form=AnswerOptionForm,
    extra=2,
    can_delete=True
)

VocabularioFormSet = inlineformset_factory(
    Audiobook,
    Vocabulario,
    form=VocabularioForm,
    extra=1,
    can_delete=True
)