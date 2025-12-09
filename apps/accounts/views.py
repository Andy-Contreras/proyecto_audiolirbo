from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            #Buscar al usuario por email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email o contraseña incorrectos.")
            return render(request, "accounts/login.html")
        
        user_auth = authenticate(request, username =user.username, password=password)
        if user_auth is not None:
            login(request, user_auth)
            return redirect("dashboard")
        else:
            messages.error(request, "Email o contraseña incorrectos.")
        
    return render(request, "accounts/login.html")
    # return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if not full_name or not email or not password or not confirm:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("register")
        
        if password != confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email ya esta registrado")
            return redirect("register")
        
        # Generemos el username automatico
        username = email.split("@")[0]

        # Asegurarme que no exista ya
        counter = 1
        base_username = username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # separa nombre completo
        full_name = full_name.strip()
        parts = full_name.split()
        if len(parts) == 1:
            first_name = parts[0]
            last_name = ""
        elif len(parts) == 2:
            first_name = parts[0]
            last_name = parts[1]
        else:
            first_name = " ".join(parts[:-2])
            last_name = " ".join(parts[-2:])


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )
        messages.success(request, "Cuenta creada con éxito, ahora inicia sesión")
        return redirect("login")
    
    return render(request, "accounts/register.html")

def logout_view(request):
    logout(request)
    return redirect("login")

