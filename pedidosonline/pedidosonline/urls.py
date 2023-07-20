"""
URL configuration for pedidosonline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from online.views import portada, registrarse, iniciar_sesion, registro_cliente, ingresar_login, mi_cuenta, salir, detalle_producto, agregar_item, carrito, confirmar_pedido, quitar_item, modificar_cantidad
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", portada, name='inicio'),
    path("registro-cliente", registrarse, name='register'),
    path("registro", registro_cliente, name='registro'),
    path("inicio-cliente", iniciar_sesion, name='login'),
    path("login", ingresar_login, name='ingresar_login'),
    path("mi-cuenta", mi_cuenta, name='mi-cuenta'),
    path('salir', salir, name='salir'),
    path('detalle-producto/<slug:slug_url>', detalle_producto, name='detalle-producto'),
    path('carrito/agregar-item', agregar_item, name="agregar_item"),
    path('carrito/quitar-item', quitar_item, name="quitar_item"),
    path('carrito', carrito, name='carrito'),
    path('confirmar-pedido', confirmar_pedido, name='confirmar-pedido'),
    path('modificar-cantidad', modificar_cantidad, name='modificar-cantidad'),
    # confirmar pedido
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
