from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from online.forms import RegistroClienteForm, LoginForm
from django.contrib.auth.models import User
from pedidos.models import Cliente
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from productos.models import Producto, Presentacion, Medida, Color
from django.core.exceptions import ObjectDoesNotExist

# portada


def portada(request):
    # consultar los registros en la tabla producto
    # select * from producto
    productos = Producto.objects.all()
    return render(request, "online/portada.html", {"lista_productos": productos})

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
    formulario = LoginForm(initial={"email": "", "password": ""})
    return render(request, "online/iniciar-sesion.html", {"formulario": formulario})

# realizar el inicio de sesion


def ingresar_login(request):
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data["email"]
            password = formulario.cleaned_data["password"]
            usuario_logeado = authenticate(username=email, password=password)
            login(request, usuario_logeado)  # es la que inicia sesion

            # mi-cuenta
            url = reverse("mi-cuenta")
            return HttpResponseRedirect(url)
        else:
            return render(request, "online/iniciar-sesion.html", {"formulario": formulario})
    else:
        url = reverse('login')
        return HttpResponseRedirect(url)


@login_required(login_url='/inicio-cliente')
def salir(request):
    logout(request)
    url = reverse('inicio')
    return HttpResponseRedirect(url)

# detalle del producto
# detalle-producto/producto-abc


def detalle_producto(request, slug_url):
    try:
        # Object Productom, Exception
        producto = Producto.objects.get(slug=slug_url)
        # imagenes
        imagenes = producto.imagen_set.order_by('orden')
        # medidas
        medidas = producto.medidas.distinct()  # lista de objetos de la clase Medida
        # colores
        colores = producto.colores.distinct()

        return render(request, "online/detalle-producto.html", {
            "producto": producto,
            "imagenes": imagenes,
            "medidas": medidas,
            "colores": colores
        })
    except ObjectDoesNotExist as error:
        return render(request, "online/404.html", {"mensaje": "El producto que buscas no existe", "detalle": "Al parecer el producto no existe o no está disponible"})

# carrito de compras
# cart.html


# confirmar pedido (proteger: no se puede acceder sino se ha iniciado sesion)
# checkout.html

# Mi cuenta
@login_required(login_url='/inicio-cliente')
def mi_cuenta(request):
    return render(request, "online/mi-cuenta.html")


def agregar_item(request):
    if request.method == 'POST':
        producto_id = int(request.POST.get('producto_id'))
        cantidad = int(request.POST.get('cantidad'))
        medida_id = int(request.POST.get('medida_id'))
        color_id = int(request.POST.get('color_id'))

        try:
            # verificar que la presentacion exista
            presentacion = Presentacion.objects.get(producto_id=producto_id,
                                                    medida_id=medida_id,
                                                    color_id=color_id)


            
            # obtener la variables "carrito"
            """
            [
                item1,
                item2,
                item3,
                ....
            ]
            
            {
                "presentacion_id": 1,
                "cantidad": 10,
                "precio": 150,
                "subtotal": 1500,
                "descripcion": Producto ABC VERDE S,
                "imagen": imagen
            }
            """
            carrito = request.session.get('carrito', [])

            precio_venta = float(presentacion.producto.precio)
            subtotal = precio_venta * float(cantidad)
            descripcion = presentacion.__str__()
            imagen = presentacion.producto.imagen_set.order_by('orden')[0].nombre.url

            elemento_nuevo = True
            posicion_existente = 0
            
            for indice, elemento in enumerate(carrito):
                if elemento["presentacion_id"] == presentacion.id:
                    elemento_nuevo = False
                    posicion_existente = indice
                    cantidad = cantidad + elemento["cantidad"]

            # verificar el stock disponible
            if elemento_nuevo:
                item = {
                    "presentacion_id": presentacion.id,
                    "cantidad": cantidad,
                    "precio": precio_venta,
                    "subtotal": subtotal,
                    "descripcion": descripcion,
                    "imagen": imagen
                }
                
                carrito.append(item)
            else:
                carrito[posicion_existente] = {
                    "presentacion_id": presentacion.id,
                    "cantidad": cantidad,
                    "precio": precio_venta,
                    "subtotal": subtotal,
                    "descripcion": descripcion,
                    "imagen": imagen
                }
            #actualizar la variable de sesion
            request.session["carrito"] = carrito
            
            #dar un mensaje
            data = {"message": 'Item agregado correctamente'}
            return JsonResponse(data, status=200)

        except ObjectDoesNotExist as error:
            data = {"message": 'Presentacion de producto no existe'}
            return JsonResponse(data, status=404)
    else:
        pass
    
def carrito(request):
    return render("online/carrito.html")
    
def confirmar_pedido(request):
    return render("online/confirmar_pedido.html")
