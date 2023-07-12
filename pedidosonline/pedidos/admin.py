from django.contrib import admin
from pedidos.models import Cliente, Pedido, DetallePedido




class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'email', 'dni', 'celular', 'direccion', 'usuario']
    search_fields = ["nombres", "apellidos", "dni"]
    fieldsets = (
        # datos personales
        ("Datos personales", {
            "fields": (
                ("apellidos", "nombres", "dni"), 
            )
        }),
        # datos de contacto
        ("Datos de contacto", {
            "fields": (
                ('email', 'celular', 'direccion')
            )
        }
        ),
        # datos de usuario
        ("Datos de usuario", {
            "fields": (
                "usuario",
            )
        }),
    )

admin.site.register(Cliente, ClienteAdmin)

class ClienteInline(admin.TabularInline):
    model = Cliente

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ["fecha", "numero", "formato_total", "cliente"]
    search_fields = ["fecha", "numero", "cliente__nombres"]
    inlines = [DetallePedidoInline]
    #autocomplete_fields=["cliente"]  #autocompletar
    raw_id_fields = ["cliente"]

admin.site.register(Pedido, PedidoAdmin)


admin.site.register(DetallePedido)



