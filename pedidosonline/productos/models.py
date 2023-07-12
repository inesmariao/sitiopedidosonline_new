from django.db import models
from autoslug import AutoSlugField

class Categoria(models.Model):
    # django por defecto agregará de manera automatica
    # la columna "id", BIGINTEGER, PRIMARY KEY, AUTOINCREMENTABLE
    nombre = models.CharField("Nombre", max_length=100)
    activo = models.BooleanField("Activo", default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "categoria"

class Marca(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    imagen = models.ImageField("Imagen", upload_to="marcas")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = "marca"

class Medida(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = "medida"
        
    
class Color(models.Model):
    nombre = models.CharField("Nombre", max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "color"
        verbose_name = "Color"
        verbose_name_plural = "Colores"

class Producto(models.Model):
    titulo = models.CharField("Titulo", max_length=200)
    slug = AutoSlugField(populate_from = 'titulo', unique=True, always_update=True)
    codigo = models.CharField("Código", max_length=50)
    precio = models.DecimalField("Precio", max_digits=9, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    marca = models.ForeignKey(Marca, on_delete=models.RESTRICT)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = "producto"

class Imagen(models.Model):
    nombre = models.ImageField("Imagen", upload_to="imagenes_productos")
    orden = models.IntegerField("Orden", null=True)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.producto.titulo + " - Imagen " + str(self.orden)
    
    class Meta:
        db_table = "imagen"
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        
class Presentacion(models.Model):
    stock = models.IntegerField("Stock")
    medida = models.ForeignKey(Medida, on_delete=models.RESTRICT)
    color = models.ForeignKey(Color, on_delete=models.RESTRICT)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)

    def __str__(self):
        return self.producto.titulo + "(" + self.medida.nombre + " - " + self.color.nombre + ")"

    class Meta:
        db_table = "presentacion"
        verbose_name = "Presentación de producto"
        verbose_name_plural = "Presentaciones de productos"