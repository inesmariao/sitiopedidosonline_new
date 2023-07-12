from django.contrib import admin
from productos.models import Categoria, Marca, Color, Medida, Producto, Imagen, Presentacion

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Color)
admin.site.register(Medida)

class ImagenInline(admin.TabularInline):
    model = Imagen

class PresentacionInline(admin.TabularInline):
    model = Presentacion
    
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "codigo", "categoria", "marca", "precio"]
    search_fields = ["titulo", "codigo", "categoria__nombre", "marca__nombre", "precio"]
    list_filter = ["categoria", "marca"]
    inlines = [ImagenInline, PresentacionInline]
    

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Imagen)



class PresentacionAdmin(admin.ModelAdmin):
    list_display = ["producto", "stock", "medida", "color"]

admin.site.register(Presentacion, PresentacionAdmin)

