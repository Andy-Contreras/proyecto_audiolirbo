from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
def evaluar_preguntas(preguntas, respuestas_post):
    puntaje_total = 0
    puntaje_maximo = 0
    detalles = []

    for pregunta in preguntas:
        correcta = pregunta.options.filter(is_correct=True).first()

        if correcta:
            puntaje_maximo += correcta.points_if_correct

        key = f"pregunta_{pregunta.id}"
        seleccion = respuestas_post.get(key)

        respuesta_correcta = correcta.text if correcta else ""
        justificacion = correcta.justification if correcta else ""

        if not seleccion:
            detalles.append({
                "pregunta": pregunta.text,
                "respuesta": "Sin respuesta",
                "correcta": False,
                "puntos": 0,
                "respuesta_correcto": respuesta_correcta,
                "justificacion": justificacion,
            })
            continue

        try:
            opcion = pregunta.options.get(id=seleccion)
        except:
            opcion = None

        if not opcion:
            detalles.append({
                "pregunta": pregunta.text,
                "respuesta": "Respuesta inválida",
                "correcta": False,
                "puntos": 0,
                "respuesta_correcto": respuesta_correcta,
                "justificacion": justificacion,
            })
            continue

        es_correcta = opcion.is_correct
        puntos = opcion.points_if_correct if es_correcta else opcion.points_if_wrong

        puntaje_total += puntos

        detalles.append({
            "pregunta": pregunta.text,
            "respuesta": opcion.text,
            "correcta": es_correcta,
            "puntos": puntos,
            "respuesta_correcto": respuesta_correcta,
            "justificacion": justificacion,
        })

    puntaje_sobre_10 = (
        round((puntaje_total / puntaje_maximo) * 10, 2)
        if puntaje_maximo > 0
        else 0
    )

    return puntaje_sobre_10, puntaje_total, puntaje_maximo, detalles





def enviar_resultado_cuestionario(resultado, detalles):
    audiobook = resultado.audiobook
    docente = audiobook.added_by

    if not docente.email:
        return

    asunto = f"Nuevo resultado - {audiobook.title}"
    fecha_local = timezone.localtime(resultado.creado_en)

    contexto = {
        "resultado": resultado,
        "audiobook": audiobook,
        "detalles": detalles,
        "fecha": fecha_local.strftime('%d/%m/%Y %H:%M'),
    }

    html_content = render_to_string(
        "emails/resultado_cuestionario.html",
        contexto
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=asunto,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[docente.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()