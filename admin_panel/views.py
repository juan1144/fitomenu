from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm


def lista_productos(request):
    productos = Producto.objects.filter(disponible=True)
    return render(
        request,
        "admin_panel/lista.html",
        {"productos": productos},  # Get products from database
    )


# Vista para crear un nuevo producto
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:lista_productos")
    else:
        form = ProductoForm()

    return render(request, "admin_panel/producto_form.html", {"form": form, "titulo": "Agregar Producto"})


# Vista para editar un producto existente
def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:lista_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "admin_panel/producto_form.html", {"form": form, "titulo": "Editar Producto"})


# Vista para eliminar un producto
def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.delete()
        return redirect("admin_panel:lista_productos")

    return render(request, "admin_panel/producto_confirm_delete.html", {"producto": producto})