import nested_admin
from django.contrib import admin
from .models import Audiobook, Questions, AnswerOption, Vocabulario


# ---------------------------
# INLINE DE OPCIONES
# ---------------------------
class AnswerOptionInline(nested_admin.NestedTabularInline):
    model = AnswerOption
    extra = 3
    fields = ("text", "is_correct","justification", "points_if_correct", "points_if_wrong")


# ---------------------------
# INLINE DE PREGUNTAS
# ---------------------------
class QuestionsInline(nested_admin.NestedStackedInline):
    model = Questions
    extra = 5  # Esto crea automáticamente 5 preguntas vacías
    fields = ("text",)
    inlines = [AnswerOptionInline]

# ---------------------------
# Inlince DEL Vocabulario 
# ---------------------------

class VocabularioInline(nested_admin.NestedTabularInline):
    model = Vocabulario
    extra = 3  # Esto solo crea 3 filas vacías por defecto
    fields = ("palabra", "definicion", "ejemplo")


# ---------------------------
# ADMIN DEL AUDIOLIBRO
# ---------------------------
@admin.register(Audiobook)
class AudiobookAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ('added_by',)
    exclude = ('added_by',)
    inlines = [QuestionsInline, VocabularioInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


# ---------------------------
# ADMIN CLÁSICOS (OPCIONAL)
# Si quieres verlos aparte
# ---------------------------
@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "audiobooks", "created_at")
    search_fields = ("text",)


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct",
                    "points_if_correct", "points_if_wrong")
    list_filter = ("is_correct",)
    search_fields = ("text",)
