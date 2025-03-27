from django import forms
from django.core.management.commands.makemessages import plural_forms_re

from .models import Producto, Orden
from .models import CategoriaProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "precio", "imagen", "disponible", "categoria"]

class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nueva categoría"})
        }

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ["numero_mesa"]
