from django.core.mail import send_mail
from django.conf import settings

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





def enviar_resultado_cuestionario(resultado):
    """
    Envía un correo al docente que subió el audiolibro
    con el resultado del cuestionario.
    """

    audiobook = resultado.audiobook
    docente = audiobook.added_by

    if not docente.email:
        return  # no hay email, no enviamos nada

    asunto = f"Nuevo resultado - {audiobook.title}"

    mensaje = f"""
Hola {docente.get_full_name() or docente.username},

Un estudiante ha completado el cuestionario de tu audiolibro.

📘 Audiolibro:
{audiobook.title}

👤 Estudiante:
Nombre: {resultado.nombre} {resultado.apellido}
Correo: {resultado.correo}

📊 Resultado:
Puntaje obtenido: {resultado.puntaje}/10

📅 Fecha:
{resultado.creado_en.strftime('%d/%m/%Y %H:%M')}

Saludos,
Plataforma de Audiolibros
"""

    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[docente.email],
        fail_silently=False,
    )