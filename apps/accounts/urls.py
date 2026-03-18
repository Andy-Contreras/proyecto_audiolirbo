from .views import login_view, register_view, logout_view
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('login/', login_view , name="login"),
    path("register/", register_view, name="register"),
    path('logout/', logout_view, name="logout"),
    # 1. Formulario para ingresar el email
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    
    # 2. Mensaje de "Email enviado"
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    
    # 3. Formulario para poner la nueva contraseña (usa un token único)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    
    # 4. Mensaje de "Contraseña cambiada con éxito"
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]