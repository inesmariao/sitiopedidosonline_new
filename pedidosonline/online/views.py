from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from online.forms import RegistroClienteForm, LoginForm
from django.contrib.auth.models import User
from pedidos.models import Cliente

# portada


def portada(request):
    return render(request, "online/portada.html")

# registrarse: mostrar la pagina para registrarse


def registrarse(request):
    return render(request, "online/registrarse.html")


# se realice el guardado en la BD
def registro_cliente(request):
    if request.method == "POST":
        # creando la relación FORM DJANGO y FORM HTML
        formulario = RegistroClienteForm(request.POST)

        if formulario.is_valid():
            nombres = formulario.cleaned_data["nombres"]
            apellidos = formulario.cleaned_data["apellidos"]
            email = formulario.cleaned_data["email"]
            password = formulario.cleaned_data["password"]

            # registrar el usuario
            # create_user -> guardar en BD un nuevo usuario -> auth_user
            usuario = User.objects.create_user(
                username=email,
                password=password,  # 123456
                first_name=nombres,
                last_name=apellidos,
                email=email,
            )

            # registrar al cliente
            # insert into cliente(nombres, apellidos, email)
            # values('Juan', 'Perez', 'jperez@gmail.com')
            cliente = Cliente()
            cliente.nombres = nombres
            cliente.apellidos = apellidos
            cliente.email = email
            cliente.usuario_id = usuario.id
            cliente.save()

            url = reverse('login')
            return HttpResponseRedirect(url)

        else:
            # mostrar los mensaje de error
            # url = reverse('register')
            # return HttpResponseRedirect(url)
            return render(request, "online/registrarse.html", {"form_django": formulario})
    else:
        url = reverse('register')
        return HttpResponseRedirect(url)

# iniciar sesión


def iniciar_sesion(request):
    formulario = LoginForm()
    return render(request, "online/iniciar-sesion.html", {"formulario": formulario})

# realizar el inicio de sesion


def ingresar_login(request):
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            pass
        else:
            return render(request, "online/iniciar-sesion.html", {"formulario": formulario})
    else:
        url = reverse('login')
        return HttpResponseRedirect(url)

# detalle del producto

# carrito de compras

# confirmar pedido

# Mi cuenta
