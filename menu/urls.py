from django.urls import path
from .views import (
    menu_lista,
    validar_orden,
    agregar_al_pedido,
    carrito_contenido,
    confirmar_pedido,
    actualizar_detalle_pedido,
    eliminar_detalle_pedido, ubicacion
)

app_name = "menu"

urlpatterns = [
    path('', menu_lista, name='menu_lista'),
    path("validar-orden/", validar_orden, name='validar_orden'),
    path("agregar/", agregar_al_pedido, name='agregar_al_pedido'),
    path("carrito/contenido/", carrito_contenido, name="carrito_contenido"),
    path("carrito/confirmar/", confirmar_pedido, name="confirmar_pedido"),
    path("carrito/actualizar/<int:detalle_id>/", actualizar_detalle_pedido, name="actualizar_detalle_pedido"),
    path("carrito/eliminar/<int:detalle_id>/", eliminar_detalle_pedido, name="eliminar_detalle_pedido"),
    path("ubicacion/", ubicacion, name="ubicacion"),
]