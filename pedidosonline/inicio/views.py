from django.shortcuts import render
from django.http import HttpResponse

def listado_usuarios(request):
    print(request.GET)
    nombre = request.GET.get("nombre", "-")
    apellido = request.GET.get("apellido", "+")
    return HttpResponse("Listado de usuarios: " + nombre + " " + apellido)

def crear_usuario(request):
    return render(request, "formulario.html", {})

def editar_usuario(request, id, tipo):
    return HttpResponse("El id del usuario es:" + str(tipo))