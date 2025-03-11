from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    disponible = models.BooleanField(default=True)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
