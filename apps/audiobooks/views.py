from django.shortcuts import render, get_object_or_404, redirect
from .models import Audiobook, AnswerOption, ResultadoCuestionario
from .utils import evaluar_preguntas, enviar_resultado_cuestionario
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.utils import timezone
from django.http import HttpResponseForbidden
from .forms import AudiobookForm
from .forms import (QuestionFormSet,
    AnswerFormSet,
    VocabularioFormSet)
# Create your views here.

@login_required
def dashboard_privado_view(request):
    total_audiolibros = Audiobook.objects.count()
    total_participantes = (
        ResultadoCuestionario.objects
        .values("correo")
        .distinct()
        .count()
    )
    practicas_completadas = ResultadoCuestionario.objects.count()
    calificacion_promedio = ResultadoCuestionario.objects.aggregate(
        promedio=Avg("puntaje")
    )["promedio"]
    # Por si no hay resultados aún
    if calificacion_promedio is None:
        calificacion_promedio = 0

    # --- Nuevos usuarios este mes ---
    now = timezone.now()
    inicio_mes = now.replace(day=1, hour=0, minute=0, second=0)

    usuarios_mes_actual = (
        ResultadoCuestionario.objects
        .filter(creado_en__gte=inicio_mes)
        .values("correo")
        .distinct()
        .count()
    )
    context = {
        "total_audiolibros": total_audiolibros,
        "total_participantes": total_participantes,
        "calificacion_promedio": round(calificacion_promedio, 1),
        "practicas_completadas":practicas_completadas,
        "usuarios_mes_actual": usuarios_mes_actual,
    }
    return render(request, "administrador/detalle_administrador.html", context)


@login_required
def nuevo_audiolibro_view(request):
    if request.method == "POST":
        form = AudiobookForm(request.POST, request.FILES)
        if form.is_valid():
            audiobook = form.save(commit=False)
            audiobook.added_by = request.user
            audiobook.save()
            return redirect("administrador")
    else:
        form = AudiobookForm()

    return render(request, 'administrador/Audiobook/crear_audiobook.html', {
        'form': form
    })


@login_required
def mis_audiolibros_view(request):
    audiolibros = Audiobook.objects.filter(added_by=request.user)

    return render(
        request,
        'administrador/Questions/inicio_preguntas.html',
        {
            'audiolibros': audiolibros
        }
    )


@login_required
def crear_contenido_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)

    # 🔐 Seguridad
    if audiobook.added_by != request.user:
        return HttpResponseForbidden("No tienes permiso")

    if request.method == 'POST':
        question_formset = QuestionFormSet(
            request.POST,
            instance=audiobook,
            prefix='questions'
        )

        answer_formsets = []

        if question_formset.is_valid():
            questions = question_formset.save()

            # 👉 Para cada pregunta, procesamos sus respuestas
            for question in questions:
                answer_formset = AnswerFormSet(
                    request.POST,
                    instance=question,
                    prefix=f'answers-{question.id}'
                )

                if answer_formset.is_valid():
                    answer_formset.save()

                answer_formsets.append((question, answer_formset))

            return redirect(
                'crear_contenido_audiobook',
                audiobook.id
            )

    else:
        question_formset = QuestionFormSet(
            instance=audiobook,
            prefix='questions'
        )

        answer_formsets = []
        for question in audiobook.questions.all():
            formset = AnswerFormSet(
                instance=question,
                prefix=f'answers-{question.id}'
            )
            answer_formsets.append((question, formset))

    return render(
        request,
        'administrador/Questions/crear_preguntas.html',
        {
            'audiobook': audiobook,
            'question_formset': question_formset,
            'answer_formsets': answer_formsets,
        }
    )




# vistas para el usuario

def dashboard_view(request):
    audiobook = Audiobook.objects.all()[:5]
    context = {
        'titulo_pagina': 'Audio Practice',
        'audiolibro': audiobook,
    }
    return render(request, "inicio/inicio.html", context)


def detalle_view(request, id):
    audiobook = get_object_or_404(Audiobook, id=id)
    preguntas = audiobook.questions.prefetch_related("options")

    # -----------------------------
    # 1. PROCESAR POST
    # -----------------------------
    if request.method == "POST":
        nombre = request.POST.get("nombre", "")
        apellido = request.POST.get("apellido", "")
        correo = request.POST.get("correo", "")

        puntaje, puntaje_real, puntaje_maximo, detalles = evaluar_preguntas(
            preguntas,
            request.POST
        )

        resultado = ResultadoCuestionario.objects.create(
            audiobook=audiobook,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            puntaje=puntaje,
        )

        # Enviar correo al docente
        enviar_resultado_cuestionario(resultado)

        # -----------------------------
        # GUARDAR RESULTADO EN SESIÓN
        # -----------------------------
        request.session["resultado_cuestionario"] = {
            "puntaje": puntaje,
            "puntaje_real": puntaje_real,
            "puntaje_maximo": puntaje_maximo,
            "detalles": detalles,
        }

        # REDIRIGIR PARA EVITAR DUPLICADOS AL RECARGAR
        return redirect("detalle", id=id)

    # -----------------------------
    # 2. PROCESAR GET (MOSTRAR RESULTADO)
    # -----------------------------
    datos_resultado = request.session.pop("resultado_cuestionario", None)

    contexto = {
        "libro": audiobook,
        "preguntas": preguntas,
        "titulo_pagina": "Audio Practice",
    }

    # Si existen datos guardados, agregarlos al contexto
    if datos_resultado:
        contexto.update(datos_resultado)

    return render(request, "inicio/detalle.html", contexto)


