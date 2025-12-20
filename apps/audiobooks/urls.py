from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # url para las personas que iniciaron sesion
    path('administrador/',views.dashboard_privado_view, name="administrador" ),
    path('audiolibros/nuevo/', views.nuevo_audiolibro_view, name='nuevo_audiolibro'),
    path('audiobooks/mis-audiolibros/',views.mis_audiolibros_view,name='mis_audiolibros'),
    path("audiobook/",views.usuarios_audiobook,name="usuarios"),
    
    # Gestionar preguntas de un audiolibro
    path('audiobook/<int:audiobook_id>/questions/', views.manage_questions, name='manage_questions'),
    
    # AJAX endpoints
    path('audiobook/<int:audiobook_id>/questions/save/', views.save_question, name='save_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('question/<int:question_id>/details/', views.question_details, name='question_details'),
    
    # Glosarios 
    path("vocabulario/", views.lista_vocabulario, name="lista_vocabulario"),
    path('audiobook/<int:audiobook_id>/vocabulario/', views.manage_vocabulary, name='manage_vocabulary'),
    
    # AJAX - Operaciones CRUD
    path('audiobook/<int:audiobook_id>/vocabulario/save/', views.save_vocabulary, name='save_vocabulary'),
    path('vocabulario/<int:vocab_id>/update/', views.update_vocabulary, name='update_vocabulary'),
    path('vocabulario/<int:vocab_id>/delete/', views.delete_vocabulary, name='delete_vocabulary'),
    path('vocabulario/<int:vocab_id>/details/', views.vocabulary_details, name='vocabulary_details'),

    path("settings/", views.settings_view, name="settings"),
    path("settings/password/", views.change_password, name="password_change"),
    
    # url para las personas que no necesitan iniciar sesion 
    path('', views.dashboard_view, name="dashboard"),
    path('detalle/<int:id>/', views.detalle_view, name="detalle"),
]