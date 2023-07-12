from django.db import models
from django.contrib.auth.models import User
from productos.models import Presentacion
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html


def validar_dni(value):
    if value is not None and value != '':
        if len(value) < 8:
            # lanzando una excepción para que pare y pida lo que se necesita
            raise ValidationError("El DNI debe tener al menos 8 caracteres")
        elif len(value) > 10:
            raise ValidationError("El DNI debe tener máximo 10 caracteres")


class Cliente(models.Model):
    nombres = models.CharField("Nombres", max_length=100)
    apellidos = models.CharField("Apellidos", max_length=100)
    email = models.EmailField("Email", max_length=70)
    direccion = models.CharField(
        "Dirección", max_length=100, null=True, blank=True)
    celular = models.CharField("Celular", max_length=20, null=True, blank=True)
    dni = models.CharField("DNI", max_length=20, null=True,
                           blank=True, validators=[validar_dni])
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    class Meta:
        db_table = "cliente"


class Pedido(models.Model):
    # fecha = models.DateField(auto_now_add=True) #no muestra la fecha para elegirla
    # quiero mostrar el campo fecha que aparezca la fecha del día de hoy
    fecha = models.DateField(default=timezone.now)
    numero = models.CharField("Número de pedido", max_length=10, editable=False)
    total = models.DecimalField("Total", max_digits=9, decimal_places=2, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    @admin.display
    def formato_total(self):
        if self.total > 100:
            return format_html("<strong style='color:green'>$ " + str(self.total) + "</strong>")
        else:
            return format_html("<strong style='color:red'>$ " + str(self.total) + "</strong>")


    def __str__(self):
        return self.numero
    
    # sobreescribir el método SAVE() registro o actualización
    def save(self):
        if self.id is None:
            self.total = 0.00
            self.numero = "00000"
        # se ejecuta el método save() de la clase padre
        return super().save()
    

    class Meta:
        db_table = "pedido"


class DetallePedido(models.Model):
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(
        "Precio Unitario", max_digits=9, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)
    presentacion = models.ForeignKey(
        Presentacion, on_delete=models.RESTRICT, verbose_name="Presentación")

    def __str__(self):
        return self.pedido.numero
    # sobreescribir el método SAVE() registro o actualización
    def save(self):
        # el pedido ya está en la BD
        if self.id is None:
            pedido_padre = self.pedido
            total = pedido_padre.total
            total = total + float(self.cantidad * self.precio_unitario)
            pedido_padre.total = total
            pedido_padre.save()
        # se ejecuta el método save() de la clase padre
        return super().save()

    class Meta:
        db_table = "detalle_pedido"
