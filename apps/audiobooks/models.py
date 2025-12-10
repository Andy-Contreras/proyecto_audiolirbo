from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.

class Audiobook(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Título"
    )

    author_name = models.CharField(
        max_length=255,
        verbose_name="Autor"
    )

    cover_image = models.ImageField(
        upload_to="audiobooks/covers/",
        verbose_name="Portada"
    )

    audio_file = models.FileField(
        upload_to="audiobooks/audio/",
        verbose_name="Archivo de audio"
    )

    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="audiobooks_uploaded",
        verbose_name="Subido por"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    def is_video(self):
        video_extensions = ['.mp4', '.webm', '.ogg']
        ext = os.path.splitext(self.audio_file.name)[1].lower()
        return ext in video_extensions

    def is_audio(self):
        audio_extensions = ['.mp3', '.wav', '.ogg']
        ext = os.path.splitext(self.audio_file.name)[1].lower()
        return ext in audio_extensions

    def __str__(self):
        return f"{self.title} - {self.author_name} - {self.added_by}"
    


class Questions(models.Model):
    audiobooks = models.ForeignKey(
        Audiobook,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Audiolibro"
    )
    text = models.CharField(max_length=500, verbose_name="Texto de la pregunta")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Pregunta"
    )
    text = models.CharField(max_length=300, verbose_name="Texto de la opción")
    is_correct = models.BooleanField(default=False, verbose_name="¿Correcta?")
    justification = models.TextField(
        blank=True,
        null=True,
        verbose_name="Justificación de la respuesta"
    )
    # Puntajes (ajusta valores por defecto si deseas penalizar respuestas erróneas)
    points_if_correct = models.IntegerField(default=1, verbose_name="Puntos si es correcta")
    points_if_wrong = models.IntegerField(default=0, verbose_name="Puntos si es incorrecta")

    class Meta:
        verbose_name = "Opción de respuesta"
        verbose_name_plural = "Opciones de respuesta"

    def __str__(self):
        return f"{self.text} ({'✔' if self.is_correct else '✖'})"
    

class ResultadoCuestionario(models.Model):
    audiobook = models.ForeignKey(Audiobook, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    correo = models.EmailField()
    puntaje = models.FloatField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.puntaje}"
    


class Vocabulario(models.Model):
    audiobook = models.ForeignKey(
        Audiobook,
        on_delete=models.CASCADE,
        related_name="vocabulario",
        verbose_name="Audiolibro"
    )
    
    palabra = models.CharField(max_length=100, verbose_name="Palabra")
    definicion = models.TextField(verbose_name="Definición")
    ejemplo = models.TextField(blank=True, null=True, verbose_name="Ejemplo de uso")

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vocabulario"
        verbose_name_plural = "Vocabularios"

    def __str__(self):
        return self.palabra
