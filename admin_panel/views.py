import datetime
import io

import pandas as pd
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.timezone import now, timedelta

from menu.models import Pedido, DetallePedido
from .models import Producto, CategoriaProducto, Orden, RestauranteInfo
from .forms import ProductoForm, CategoriaProductoForm, OrdenForm, RestauranteInfoForm


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

        return render(
            request, "admin_panel/partials/_orden_toggle_row.html", {"orden": orden}
        )
    return JsonResponse({"success": False, "error": "Método no permitido"})


def editar_info_restaurante(request):
    instance, _ = RestauranteInfo.objects.get_or_create(id=1)

    if request.method == "POST":
        form = RestauranteInfoForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:editar_info_restaurante")
    else:
        form = RestauranteInfoForm(instance=instance)

    return render(
        request,
        "admin_panel/info_restaurante_form.html",
        {
            "form": form,
            "page_title": "Configuración del Restaurante",
            "show_sidebar": False,
        },
    )


def dashboard(request: HttpRequest):
    hoy = now().date()
    rangos = [
        (hoy - timedelta(days=7 * i), hoy - timedelta(days=7 * (i + 1)))
        for i in range(5)
    ]

    siete_dias_atras = hoy - timedelta(days=7)
    top_productos = (
        DetallePedido.objects.filter(
            pedido__created_at__date__gte=siete_dias_atras, pedido__estado="entregado"
        )
        .values("producto__nombre")
        .annotate(total_cantidad=Sum("cantidad"))
        .order_by("-total_cantidad")[:5]
    )
    top_nombres = [p["producto__nombre"] for p in top_productos]

    producto_semana_data = {nombre: [] for nombre in top_nombres}
    for inicio, fin in rangos:
        semana_detalles = (
            DetallePedido.objects.filter(
                pedido__created_at__date__gte=fin,
                pedido__created_at__date__lt=inicio,
                pedido__estado="entregado",
                producto__nombre__in=top_nombres,
            )
            .values("producto__nombre")
            .annotate(cantidad=Sum("cantidad"))
        )
        cantidades = {d["producto__nombre"]: d["cantidad"] for d in semana_detalles}
        for nombre in top_nombres:
            producto_semana_data[nombre].append(cantidades.get(nombre, 0))

    ganancias = []
    etiquetas = []
    for inicio, fin in rangos:
        semana_total = (
            Pedido.objects.filter(
                created_at__date__gte=fin,
                created_at__date__lt=inicio,
                estado="entregado",
            ).aggregate(total=Sum("precio_total"))["total"]
            or 0
        )
        ganancias.append(float(semana_total))
        etiquetas.append(f"{(hoy - inicio).days}-{(hoy - fin).days}")

    # ========== REPORTE ==========
    desde_str = request.GET.get("desde")
    hasta_str = request.GET.get("hasta")
    try:
        desde = (
            datetime.datetime.strptime(desde_str, "%Y-%m-%d").date()
            if desde_str
            else hoy - timedelta(days=7)
        )
        hasta = (
            datetime.datetime.strptime(hasta_str, "%Y-%m-%d").date()
            if hasta_str
            else hoy
        )
    except ValueError:
        desde = hoy - timedelta(days=7)
        hasta = hoy

    pedidos = (
        Pedido.objects.filter(created_at__date__range=[desde, hasta])
        .select_related("orden")
        .annotate(
            total_items=Sum("detalles__cantidad"),
            productos_unicos=Count("detalles__producto", distinct=True),
        )
        .order_by("-created_at")
    )

    # ========== EXPORTACIÓN ==========
    if request.GET.get("exportar") == "1":
        data = []
        for i, p in enumerate(pedidos, start=1):
            data.append(
                {
                    "#": i,
                    "Fecha": p.created_at.strftime("%d/%m/%Y"),
                    "Productos únicos": p.productos_unicos,
                    "Total ítems": p.total_items,
                    "Total cancelado": float(p.precio_total),
                }
            )

        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Órdenes")
        output.seek(0)
        filename = f"reporte_ordenes_{desde}_{hasta}.xlsx"
        return FileResponse(output, as_attachment=True, filename=filename)

    # ========== RENDER NORMAL ==========
    return render(
        request,
        "admin_panel/dashboard.html",
        {
            "page_title": "Dashboard",
            "productos_top": top_nombres,
            "producto_semana_data": producto_semana_data,
            "ganancias": ganancias,
            "labels_ganancia": etiquetas,
            "pedidos": pedidos,
            "desde": desde,
            "hasta": hasta,
            "show_sidebar": False,
        },
    )
