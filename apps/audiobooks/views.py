from django.shortcuts import render, get_object_or_404, redirect
from .models import Audiobook, AnswerOption, ResultadoCuestionario, Vocabulario
from .utils import evaluar_preguntas, enviar_resultado_cuestionario
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Count
from django.utils import timezone
from .forms import AudiobookForm, Questions
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import CustomPasswordChangeForm
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
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
    
    if calificacion_promedio is None:
        calificacion_promedio = 0

    now = timezone.now()
    inicio_mes = now.replace(day=1, hour=0, minute=0, second=0)

    usuarios_mes_actual = (
        ResultadoCuestionario.objects
        .filter(creado_en__gte=inicio_mes)
        .values("correo")
        .distinct()
        .count()
    )

    # --- DATOS PARA EL GRÁFICO ---
    seis_meses_atras = now - timedelta(days=180)
    
    usuarios_por_mes = (
        ResultadoCuestionario.objects
        .filter(creado_en__gte=seis_meses_atras)
        .annotate(mes=TruncMonth('creado_en'))
        .values('mes')
        .annotate(total=Count('correo', distinct=True))
        .order_by('mes')
    )

    # Meses en español
    MESES = {
        1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
    }

    meses_labels = []
    meses_data = []
    
    # Crear diccionario con todos los meses
    meses_dict = {}
    for i in range(5, -1, -1):
        mes = now - timedelta(days=30*i)
        mes_key = mes.strftime('%Y-%m-01')
        meses_dict[mes_key] = 0
    
    # Llenar con datos reales
    for item in usuarios_por_mes:
        mes_key = item['mes'].strftime('%Y-%m-01')
        if mes_key in meses_dict:
            meses_dict[mes_key] = item['total']
    
    # Formatear para el gráfico
    for mes_str, total in sorted(meses_dict.items()):
        mes_obj = datetime.strptime(mes_str, '%Y-%m-%d')
        mes_numero = mes_obj.month
        anio = mes_obj.year
        
        # Formato: "Ene 2024"
        label = f"{MESES[mes_numero]} {anio}"
        
        meses_labels.append(label)
        meses_data.append(total)

    context = {
        "total_audiolibros": total_audiolibros,
        "total_participantes": total_participantes,
        "calificacion_promedio": round(calificacion_promedio, 1),
        "practicas_completadas": practicas_completadas,
        "usuarios_mes_actual": usuarios_mes_actual,
        "meses_labels": json.dumps(meses_labels),
        "meses_data": json.dumps(meses_data),
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


# Parte de la lista de audiolibros 
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

# Vista 2: Gestionar preguntas de un audiolibro (reemplaza tu crear_contenido_audiobook)
@login_required
def manage_questions(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id, added_by=request.user)
    questions = Questions.objects.filter(audiobooks=audiobook).prefetch_related('options')
    
    context = {
        'audiobook': audiobook,
        'questions': questions,
    }
    return render(request, 'administrador/Questions/crear_preguntas.html', context)

# Vista 3: Guardar pregunta (AJAX)
@login_required
@require_http_methods(["POST"])
def save_question(request, audiobook_id):
    try:
        audiobook = get_object_or_404(Audiobook, id=audiobook_id, added_by=request.user)
        data = json.loads(request.body)
        
        # Crear o actualizar la pregunta
        question_id = data.get('question_id')
        if question_id:
            question = get_object_or_404(Questions, id=question_id, audiobooks=audiobook)
            question.text = data['question_text']
            question.save()
            # Eliminar opciones antiguas
            question.options.all().delete()
        else:
            question = Questions.objects.create(
                audiobooks=audiobook,
                text=data['question_text']
            )
        
        # Crear las opciones de respuesta
        for option_data in data['options']:
            AnswerOption.objects.create(
                question=question,
                text=option_data['text'],
                is_correct=option_data['is_correct'],
                justification=option_data.get('justification', ''),
                points_if_correct=option_data.get('points_if_correct', 1),
                points_if_wrong=option_data.get('points_if_wrong', 0)
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Pregunta guardada exitosamente',
            'question_id': question.id
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

# Vista 4: Eliminar pregunta (AJAX)
@login_required
@require_http_methods(["POST"])
def delete_question(request, question_id):
    try:
        question = get_object_or_404(Questions, id=question_id)
        # Verificar que la pregunta pertenece a un audiobook del usuario
        if question.audiobooks.added_by != request.user:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permiso para eliminar esta pregunta'
            }, status=403)
        
        question.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Pregunta eliminada exitosamente'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

# Vista 5: Obtener detalles de pregunta para edición (AJAX)
@login_required
def question_details(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    
    # Verificar que la pregunta pertenece a un audiobook del usuario
    if question.audiobooks.added_by != request.user:
        return JsonResponse({
            'success': False,
            'message': 'No tienes permiso'
        }, status=403)
    
    options = question.options.all()
    
    data = {
        'id': question.id,
        'text': question.text,
        'options': [
            {
                'text': opt.text,
                'is_correct': opt.is_correct,
                'justification': opt.justification,
                'points_if_correct': opt.points_if_correct,
                'points_if_wrong': opt.points_if_wrong
            }
            for opt in options
        ]
    }
    
    return JsonResponse(data)



@login_required
def usuarios_audiobook(request):
    resultados = (
        ResultadoCuestionario.objects
        .values("nombre", "apellido", "correo")
        .annotate(
            mejor_puntaje=Max("puntaje"),
            intentos=Count("id")
        )
        .order_by("-mejor_puntaje")
    )

    return render(
        request,
        "administrador/Usuarios/inicio_usuario.html",
        {
            "resultados": resultados,
        }
    )



# vistas para el vocabulario 
@login_required
def lista_vocabulario(request):
    """Vista para listar todos los audiolibros del usuario"""
    audiolibros = Audiobook.objects.filter(added_by=request.user)
    return render(request, "administrador/Glosario/inicio_glosario.html", {
        "audiolibros": audiolibros
    })

@login_required
def manage_vocabulary(request, audiobook_id):
    """Vista principal para gestionar el vocabulario de un audiolibro"""
    audiobook = get_object_or_404(Audiobook, id=audiobook_id, added_by=request.user)
    vocabulario = Vocabulario.objects.filter(audiobook=audiobook).order_by('-creado_en')
    
    context = {
        'audiobook': audiobook,
        'vocabulario': vocabulario,
    }
    return render(request, 'administrador/Glosario/crear_glosario.html', context)

@login_required
@require_http_methods(["POST"])
def save_vocabulary(request, audiobook_id):
    """Guardar múltiples palabras del vocabulario a la vez (AJAX)"""
    try:
        audiobook = get_object_or_404(Audiobook, id=audiobook_id, added_by=request.user)
        data = json.loads(request.body)
        
        vocabulario_list = data.get('vocabulario', [])
        
        if not vocabulario_list:
            return JsonResponse({
                'success': False,
                'message': 'No se proporcionaron palabras para guardar'
            }, status=400)
        
        created_count = 0
        errors = []
        
        for vocab_data in vocabulario_list:
            palabra = vocab_data.get('palabra', '').strip()
            definicion = vocab_data.get('definicion', '').strip()
            ejemplo = vocab_data.get('ejemplo', '').strip()
            
            # Validar que tenga al menos palabra y definición
            if not palabra or not definicion:
                errors.append(f"Palabra '{palabra or 'vacía'}' omitida: faltan datos requeridos")
                continue
            
            # Verificar si ya existe
            if Vocabulario.objects.filter(audiobook=audiobook, palabra__iexact=palabra).exists():
                errors.append(f"Palabra '{palabra}' ya existe en este audiolibro")
                continue
            
            # Crear vocabulario
            Vocabulario.objects.create(
                audiobook=audiobook,
                palabra=palabra,
                definicion=definicion,
                ejemplo=ejemplo
            )
            created_count += 1
        
        message = f'{created_count} palabra(s) guardada(s) exitosamente'
        if errors:
            message += f'. {len(errors)} omitida(s)'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'created_count': created_count,
            'errors': errors
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Datos JSON inválidos'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al guardar: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def update_vocabulary(request, vocab_id):
    """Actualizar una palabra específica (AJAX)"""
    try:
        vocabulario = get_object_or_404(Vocabulario, id=vocab_id)
        
        # Verificar permisos
        if vocabulario.audiobook.added_by != request.user:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permiso para editar esta palabra'
            }, status=403)
        
        data = json.loads(request.body)
        
        vocabulario.palabra = data.get('palabra', vocabulario.palabra).strip()
        vocabulario.definicion = data.get('definicion', vocabulario.definicion).strip()
        vocabulario.ejemplo = data.get('ejemplo', '').strip()
        vocabulario.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Palabra actualizada exitosamente',
            'vocab': {
                'id': vocabulario.id,
                'palabra': vocabulario.palabra,
                'definicion': vocabulario.definicion,
                'ejemplo': vocabulario.ejemplo
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al actualizar: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def delete_vocabulary(request, vocab_id):
    """Eliminar una palabra del vocabulario (AJAX)"""
    try:
        vocabulario = get_object_or_404(Vocabulario, id=vocab_id)
        
        # Verificar permisos
        if vocabulario.audiobook.added_by != request.user:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permiso para eliminar esta palabra'
            }, status=403)
        
        palabra = vocabulario.palabra
        vocabulario.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Palabra "{palabra}" eliminada exitosamente'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar: {str(e)}'
        }, status=500)

@login_required
def vocabulary_details(request, vocab_id):
    """Obtener detalles de una palabra para edición (AJAX)"""
    try:
        vocabulario = get_object_or_404(Vocabulario, id=vocab_id)
        
        # Verificar permisos
        if vocabulario.audiobook.added_by != request.user:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permiso'
            }, status=403)
        
        return JsonResponse({
            'success': True,
            'id': vocabulario.id,
            'palabra': vocabulario.palabra,
            'definicion': vocabulario.definicion,
            'ejemplo': vocabulario.ejemplo or ''
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)
    """Obtener detalles de una palabra para edición (AJAX)"""
    try:
        vocabulario = get_object_or_404(Vocabulario, id=vocab_id)
        
        # Verificar que el vocabulario pertenece a un audiobook del usuario
        if vocabulario.audiobook.added_by != request.user:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permiso para acceder a esta palabra'
            }, status=403)
        
        data = {
            'success': True,
            'id': vocabulario.id,
            'palabra': vocabulario.palabra,
            'definicion': vocabulario.definicion,
            'ejemplo': vocabulario.ejemplo or ''
        }
        
        return JsonResponse(data)
    
    except Vocabulario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'La palabra no existe'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener detalles: {str(e)}'
        }, status=500)




# vistas para el usuario
def dashboard_view(request):
    audiobook = Audiobook.objects.all()[:10]
    context = {
        'titulo_pagina': 'Audio Practice',
        'audiolibro': audiobook,
    }
    return render(request, "inicio/inicio.html", context)

# detalle de la pagina de usuario
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


# Configuracion del administrador

@login_required
def settings_view(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

        messages.success(request, "Datos actualizados correctamente")
        return redirect("settings")

    return render(request, "administrador/settings.html")
# Contraseña nueva
@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(
                request,
                "✅ Contraseña cambiada correctamente"
            )

            return redirect("settings")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "administrador/password_change.html", {
        "form": form
    })