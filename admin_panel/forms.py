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
        fields = ["numero_mesa", "tipo"]


class RestauranteInfoForm(forms.ModelForm):
    class Meta:
        model = RestauranteInfo
        fields = [
            "nombre",
            "eslogan",
            "historia",
            "iframe_ubicacion",
            "ubicacion",
            "facebook_url",
            "instagram_url",
            "telefono",
            "correo",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "eslogan": forms.TextInput(attrs={"class": "form-control"}),
            "historia": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "iframe_ubicacion": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "ubicacion": forms.TextInput(attrs={"class": "form-control"}),
            "facebook_url": forms.URLInput(attrs={"class": "form-control"}),
            "instagram_url": forms.URLInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
        }
