from django.urls import path
from .views import lista_productos

app_name = "admin_panel"

urlpatterns = [
    path("productos/", lista_productos, name="lista_productos"),
]
