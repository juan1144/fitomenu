from django.db import models

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, related_name="productos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    orden = models.IntegerField(unique=True)
    numero_mesa = models.IntegerField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden {self.orden} - Mesa {self.mesa}"
