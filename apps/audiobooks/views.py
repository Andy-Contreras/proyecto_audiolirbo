from django.shortcuts import render, get_object_or_404
from .models import Audiobook, AnswerOption, ResultadoCuestionario
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
    preguntas = audiobook.questions.all().prefetch_related("options")

    if request.method == "POST":

        # ========= OBTENER DATOS DEL MODAL =========
        nombre = request.POST.get("nombre", "")
        apellido = request.POST.get("apellido", "")
        correo = request.POST.get("correo", "")

        puntaje_total = 0
        puntaje_maximo = 0
        detalle = []

        for pregunta in preguntas:

            # Obtener la opción correcta
            opcion_correcta = pregunta.options.filter(is_correct=True).first()
            if opcion_correcta:
                puntaje_maximo += opcion_correcta.points_if_correct

            texto_respuesta_correcta = opcion_correcta.text if opcion_correcta else ""

            key = f"pregunta_{pregunta.id}"
            seleccionar = request.POST.get(key)

            if seleccionar:
                try:
                    opcion_seleccionada = pregunta.options.get(id=seleccionar)
                except (AnswerOption.DoesNotExist, ValueError):
                    opcion_seleccionada = None

                if opcion_seleccionada:
                    correcta_flag = opcion_seleccionada.is_correct
                    puntos = opcion_seleccionada.points_if_correct if correcta_flag else opcion_seleccionada.points_if_wrong
                    puntaje_total += puntos

                    detalle.append({
                        "pregunta": pregunta.text,
                        "respuesta": opcion_seleccionada.text,
                        "correcta": correcta_flag,
                        "puntos": puntos,
                        "respuesta_correcto": texto_respuesta_correcta
                    })
                else:
                    detalle.append({
                        "pregunta": pregunta.text,
                        "respuesta": "Respuesta inválida",
                        "correcta": False,
                        "puntos": 0,
                        "respuesta_correcto": texto_respuesta_correcta
                    })

            else:
                detalle.append({
                    "pregunta": pregunta.text,
                    "respuesta": "Sin respuesta",
                    "correcta": False,
                    "puntos": 0,
                    "respuesta_correcto": texto_respuesta_correcta
                })

        # Evita división entre cero
        if puntaje_maximo > 0:
            puntaje_sobre_10 = round((puntaje_total / puntaje_maximo) * 10, 2)
        else:
            puntaje_sobre_10 = 0

        # ========= GUARDAR EN EL MODELO =========
        ResultadoCuestionario.objects.create(
            audiobook=audiobook,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            puntaje=puntaje_sobre_10
        )

        # ========= RENDERIZAR RESULTADOS =========
        return render(request, "inicio/detalle.html", {
            'libro': audiobook,
            'preguntas': preguntas,
            'puntaje': puntaje_sobre_10,
            'puntaje_real': puntaje_total,
            'puntaje_maximo': puntaje_maximo,
            'detalles': detalle,
            'titulo_pagina': 'Audio Practice',
            "nombre": nombre,       # por si quieres mostrarlo
            "apellido": apellido,
            "correo": correo,
        })

    # GET normal
    return render(request, "inicio/detalle.html", {
        'libro': audiobook,
        'preguntas': preguntas,
        'titulo_pagina': 'Audio Practice',
    })




