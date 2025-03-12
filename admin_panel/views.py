from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Producto, CategoriaProducto
from .forms import ProductoForm, CategoriaProductoForm

def lista_productos(request):
    productos_list = Producto.objects.filter(disponible=True)
    categorias = CategoriaProducto.objects.all()  # 🔹 Asegurar que enviamos las categorías al template
    paginator = Paginator(productos_list, 5)

    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    return render(
        request,
        "admin_panel/lista.html",
        {
            "productos": productos,
            "categorias": categorias,  # 🔹 Enviar las categorías
            "show_sidebar": False,
        },
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

def administrar_categorias(request):
    categorias = CategoriaProducto.objects.all()
    form = CategoriaProductoForm()
    return render(request, "admin_panel/categorias_modal.html", {"categorias": categorias, "form": form})

def cambiar_estado_categoria(request, categoria_id):
    if request.method == "POST":
        data = json.loads(request.body)
        nuevo_estado = data.get("disponible", None)

        if nuevo_estado is None:
            return JsonResponse({"success": False, "error": "Estado inválido"})

        categoria = get_object_or_404(CategoriaProducto, id=categoria_id)
        categoria.disponible = nuevo_estado  # 🔹 Cambiar estado en la base de datos
        categoria.save()

        return JsonResponse({"success": True, "nuevo_estado": categoria.disponible})

    return JsonResponse({"success": False, "error": "Método no permitido"})

def agregar_categoria(request):
    if request.method == "POST":
        form = CategoriaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": form.errors})
    return JsonResponse({"success": False, "error": "Solicitud inválida"})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(CategoriaProducto, id=categoria_id)

    if categoria.productos.exists():  # 🔹 Si tiene productos, no permitir eliminarla
        return JsonResponse({"success": False, "error": "No puedes eliminar esta categoría porque tiene productos asociados."})

    categoria.delete()
    return JsonResponse({"success": True})