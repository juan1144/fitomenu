from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Producto, CategoriaProducto, Orden
from .forms import ProductoForm, CategoriaProductoForm, OrdenForm


def lista_productos(request):
    productos_list = Producto.objects.filter(disponible=True)
    categorias = CategoriaProducto.objects.all()
    paginator = Paginator(productos_list, 5)

    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    return render(
        request,
        "admin_panel/lista.html",
        {
            "page_title": "Administración de Productos",
            "productos": productos,
            "categorias": categorias,
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

    return render(
        request,
        "admin_panel/producto_form.html",
        {
            "form": form,
            "titulo": "Agregar Producto",
            "show_sidebar": False,
        },
    )


def producto_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:lista_productos")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        "admin_panel/producto_form.html",
        {
            "form": form,
            "titulo": "Editar Producto",
            "show_sidebar": False,
        },
    )


def producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.delete()
        return HttpResponseRedirect(reverse("admin_panel:lista_productos"))


def administrar_categorias(request):
    categorias = CategoriaProducto.objects.all()
    form = CategoriaProductoForm()
    return render(
        request,
        "admin_panel/categorias_modal.html",
        {"categorias": categorias, "form": form},
    )


def cambiar_estado_categoria(request, categoria_id):
    if request.method == "POST":
        data = json.loads(request.body)
        nuevo_estado = data.get("disponible", None)

        if nuevo_estado is None:
            return JsonResponse({"success": False, "error": "Estado inválido"})

        categoria = get_object_or_404(CategoriaProducto, id=categoria_id)
        categoria.disponible = nuevo_estado
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

    if categoria.productos.exists():
        return JsonResponse(
            {
                "success": False,
                "error": "No puedes eliminar esta categoría porque tiene productos asociados.",
            }
        )

    categoria.delete()
    return JsonResponse({"success": True})


def lista_ordenes(request):
    list = Orden.objects.all().order_by("-created_at")
    paginator = Paginator(list, 10)
    page = request.GET.get("page")
    ordenes = paginator.get_page(page)

    return render(
        request,
        "admin_panel/orden_lista.html",
        {
            "page_title": "Administración de órdenes",
            "ordenes": ordenes,
            "show_sidebar": False,
        },
    )


def orden_form_modal(request):
    form = OrdenForm()
    html = render_to_string(
        "admin_panel/partials/_orden_form.html",
        {"form": form},
        request=request,
    )
    return HttpResponse(html)


def crear_orden(request):
    if request.method == "POST":
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.estado = True  # aseguramos que se cree activa
            orden.save()
            if request.headers.get("Hx-Request"):
                response = HttpResponse()
                response["HX-Trigger"] = "ordenCreada"
                return response
            return redirect("admin_panel:lista_ordenes")
    else:
        form = OrdenForm()

    html = render_to_string(
        "admin_panel/partials/_orden_form.html",
        {"form": form},
        request=request,
    )
    return HttpResponse(html)


def cambiar_estado_orden(request, orden_id):
    if request.method == "POST":
        orden = get_object_or_404(Orden, id=orden_id)
        orden.estado = not orden.estado
        orden.save()

        html = render_to_string(
            "admin_panel/partials/_orden_row.html", {"orden": orden}, request=request
        )
        return HttpResponse(html)
    return JsonResponse({"success": False, "error": "Método no permitido"})
