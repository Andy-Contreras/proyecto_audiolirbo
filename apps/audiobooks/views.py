from django.shortcuts import render, get_object_or_404
from .models import Audiobook, AnswerOption, ResultadoCuestionario
from .utils import evaluar_preguntas, enviar_resultado_cuestionario
# Create your views here.
def dashboard_view(request):
    audiobook = Audiobook.objects.all()
    query = request.GET.get("q")
    if query:
        audiobook = Audiobook.objects.filter(title__icontains=query)
    else:
        audiobook = Audiobook.objects.all()
    context = {
        'titulo_pagina': 'Audio Practice',
        'audiolibro': audiobook,
        'query': query,
    }
    return render(request, "inicio/inicio.html", context)


def detalle_view(request, id):
    audiobook = get_object_or_404(Audiobook, id=id)
    preguntas = audiobook.questions.prefetch_related("options")

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
        # ✅ Enviar correo al docente (utils.py)
        enviar_resultado_cuestionario(resultado)
        return render(request, "inicio/detalle.html", {
            "libro": audiobook,
            "preguntas": preguntas,
            "puntaje": puntaje,
            "puntaje_real": puntaje_real,
            "puntaje_maximo": puntaje_maximo,
            "detalles": detalles,
            "titulo_pagina": "Audio Practice",
        })

    return render(request, "inicio/detalle.html", {
        "libro": audiobook,
        "preguntas": preguntas,
        "titulo_pagina": "Audio Practice",
    })


