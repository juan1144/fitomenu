from django.db import models
from admin_panel.models import Producto

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('preparacion', 'En preparación'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado')
    ]

    numero_mesa = models.IntegerField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='preparacion')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.numero_mesa} - {self.get_estado_display()}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.producto.precio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Pedido {self.pedido.id})"
