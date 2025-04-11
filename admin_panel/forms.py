from django import forms

from .models import Producto, Orden, RestauranteInfo
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
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nueva categoría"}
            )
        }


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ["numero_mesa"]


class RestauranteInfoForm(forms.ModelForm):
    class Meta:
        model = RestauranteInfo
        fields = ["nombre", "eslogan", "historia", "iframe_ubicacion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "eslogan": forms.TextInput(attrs={"class": "form-control"}),
            "historia": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "iframe_ubicacion": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }
