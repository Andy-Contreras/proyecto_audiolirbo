from django.urls import path
from .views import *
urlpatterns = [
    # url para las personas que iniciaron sesion
    path('administrador/',dashboard_privado_view, name="administrador" ),
    path('audiolibros/nuevo/', nuevo_audiolibro_view, name='nuevo_audiolibro'),
    path('audiobooks/mis-audiolibros/',mis_audiolibros_view,name='mis_audiolibros'),
    path('audiobook/<int:audiobook_id>/contenido/',crear_contenido_audiobook,name='crear_contenido_audiobook'),
    # url para las personas que no necesitan iniciar sesion 
    path('', dashboard_view, name="dashboard"),
    path('detalle/<int:id>/', detalle_view, name="detalle"),
]