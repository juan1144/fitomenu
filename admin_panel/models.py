from django.db import models
from django.utils.timezone import now


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Function to show category info"""
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        CategoriaProducto, on_delete=models.CASCADE, related_name="productos"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Function to show product info"""
        return self.nombre


class Orden(models.Model):
    # orden = models.IntegerField(unique=True)
    orden = models.CharField(max_length=10)
    numero_mesa = models.IntegerField()
    tipo = models.CharField(
        max_length=1, choices=[("A", "Restaurante"), ("P", "Para llevar")]
    )
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generar_codigo(self):
        hoy = now().date()
        ultimo = Orden.objects.filter(created_at__date=hoy, tipo=self.tipo).order_by(
            "-created_at"
        )

        if ultimo.exists():
            ultimo_cod = ultimo.first().orden
            ultimo_num = int(ultimo_cod[1:])
            nuevo_num = ultimo_num + 1
        else:
            nuevo_num = 1
        return f"{self.tipo}{nuevo_num}"

    def save(self, *args, **kwargs):
        if not self.orden:
            self.orden = self.generar_codigo()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden {self.orden} - Mesa {self.numero_mesa}"


class RestauranteInfo(models.Model):
    nombre = models.CharField(max_length=255)
    eslogan = models.CharField(max_length=255, blank=True)
    historia = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=255, blank=True)
    iframe_ubicacion = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Configuración del Restaurante"

    class Meta:
        verbose_name = "Información del Restaurante"
        verbose_name_plural = "Información del Restaurante"
