from django.urls import path
from .views import (Menu_Productos, agregar_al_carrito, ver_carrito, 
modificar_carrito, obtener_carrito_actual,quitar_del_carrito,eliminar_del_carrito, marcar_pedido_entregado)
app_name = "menu"

urlpatterns = [
    path('', Menu_Productos, name='Menu_Productos'),
    path('carrito/<int:producto_id>/<int:numero_mesa>/<int:cantidad>/', agregar_al_carrito, name='Carrito'),
    path('carrito/modificar/<int:producto_id>/<int:numero_mesa>/<int:cantidad>/', modificar_carrito, name='modificar_carrito'),
    path('ver_carrito/<int:numero_mesa>/', ver_carrito, name='ver_carrito'),
    path("carrito_actual/", obtener_carrito_actual, name="carrito_actual"),
    path('carrito/quitar/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('pedido/entregado/<int:pedido_id>/', marcar_pedido_entregado, name='marcar_pedido_entregado'),
    path('categoria/<str:categoria>/', Menu_Productos, name='menu_por_categoria'),
]
