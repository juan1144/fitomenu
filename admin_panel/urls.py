from django.urls import path
from .views import lista_productos, producto_eliminar, producto_editar, producto_crear

app_name = "admin_panel"

urlpatterns = [
    path("productos/", lista_productos, name="lista_productos"),
    path("productos/agregar/", producto_crear, name="producto_crear"),
    path("productos/editar/<int:producto_id>/", producto_editar, name="producto_editar"),
    path("productos/eliminar/<int:producto_id>/", producto_eliminar, name="producto_eliminar"),
]
