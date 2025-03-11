from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.core.paginator import Paginator
from .models import Producto
from .forms import ProductoForm


def lista_productos(request):
    productos_list = Producto.objects.filter(disponible=True)
    paginator = Paginator(productos_list, 5)

    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)
    return render(
        request,
        "admin_panel/lista.html",
        {"productos": productos,
         "show_sidebar": False,},
    )

def producto_form(request):
    form = ProductoForm()
    return render(request, "admin_panel/producto_form.html", {"form": form})

def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:lista_productos")
    else:
        form = ProductoForm()

    return render(request, "admin_panel/producto_form.html", {"form": form, "titulo": "Agregar Producto", "show_sidebar": False,})

def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:lista_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "admin_panel/producto_form.html", {"form": form, "titulo": "Editar Producto", "show_sidebar": False,})

def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.delete()
        return HttpResponseRedirect(reverse('admin_panel:lista_productos'))
