from django.urls import path
from .views import Menu_Productos, agregar_al_carrito, ver_carrito
app_name = "menu"

urlpatterns = [
    path('menu/', Menu_Productos, name='Menu_Productos'),
    path('carrito/<int:producto_id>/<int:numero_mesa>/<int:cantidad>/', agregar_al_carrito, name='Carrito'),
    path('ver_carrito/<int:numero_mesa>/', ver_carrito, name='ver_carrito'),
]
