from django.urls import path
from .views import lista_productos, producto_eliminar, producto_editar, producto_crear, producto_form
from .views import administrar_categorias, cambiar_estado_categoria, agregar_categoria, eliminar_categoria
app_name = "admin_panel"

urlpatterns = [
    path("productos/", lista_productos, name="lista_productos"),
    path("productos/form/", producto_form, name="producto_form"),
    path("productos/agregar/", producto_crear, name="producto_crear"),
    path("productos/editar/<int:producto_id>/", producto_editar, name="producto_editar"),
    path("productos/eliminar/<int:producto_id>/", producto_eliminar, name="producto_eliminar"),
    path("categorias/", administrar_categorias, name="administrar_categorias"),
    path("categorias/cambiar-estado/<int:categoria_id>/", cambiar_estado_categoria, name="cambiar_estado_categoria"),
    path("categorias/agregar/", agregar_categoria, name="agregar_categoria"),
    path("categorias/eliminar/<int:categoria_id>/", eliminar_categoria, name="eliminar_categoria"),
]
