from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from admin_panel.models import Orden, Producto, CategoriaProducto


from django.urls import reverse

from .models import DetallePedido
from menu.models import Pedido


def menu_lista(request):
    orden_obj = None
    orden_valida = False
    orden_pk = request.session.get("orden_pk")

    if orden_pk:
        orden_obj = Orden.objects.filter(id=orden_pk, estado=True).first()
        if orden_obj:
            orden_valida = True

    categoria_nombre = request.GET.get("categoria")
    productos = Producto.objects.filter(disponible=True).select_related("categoria")
    if categoria_nombre:
        productos = productos.filter(categoria__nombre=categoria_nombre)

    categorias = CategoriaProducto.objects.filter(disponible=True)

    menus = [{"title": "Categorías", "is_active": True, "submenus": []}]

    menus[0]["submenus"].append(
        {
            "title": "Todos",
            "url": reverse("menu:menu_lista"),
            "is_active": not categoria_nombre,
        }
    )

    for categoria in categorias:
        menus[0]["submenus"].append(
            {
                "title": categoria.nombre,
                "url": f"{reverse('menu:menu_lista')}?categoria={categoria.nombre}",
                "is_active": categoria_nombre == categoria.nombre,
            }
        )

    return render(
        request,
        "menu/menu_lista.html",
        {
            "productos": productos,
            "categorias": categorias,
            "orden_valida": orden_valida,
            "orden_obj": orden_obj,
            "categoria_actual": categoria_nombre,
            "show_sidebar": True,
            "menus": menus,
            "page_title": "Menú",
            "show_footer": True,
        },
    )


@require_POST
def validar_orden(request):
    orden_id = request.POST.get("orden_id")

    orden = Orden.objects.filter(orden=orden_id, estado=True).first()
    if orden:
        request.session["orden_pk"] = orden.id
        html = "<div class='text-success'>Orden válida. Puedes cerrar este mensaje.</div><script>setTimeout(() => location.reload(), 1000);</script>"
    else:
        html = "<div class='text-danger'>Orden no encontrada o inactiva.</div>"

    return HttpResponse(html)


@require_POST
def agregar_al_pedido(request):
    orden_pk = request.session.get("orden_pk")
    producto_id = request.POST.get("producto_id")
    cantidad = int(request.POST.get("cantidad", 1))

    orden = Orden.objects.filter(id=orden_pk, estado=True).first()
    producto = Producto.objects.filter(id=producto_id, disponible=True).first()

    if not orden or not producto:
        return JsonResponse({"success": False, "message": "Orden o producto inválido."})

    pedido = (
        Pedido.objects.filter(orden=orden, estado__in=["confirmacion", "preparacion"])
        .order_by("-created_at")
        .first()
    )

    if not pedido:
        pedido = Pedido.objects.create(
            orden=orden, estado="confirmacion", numero_mesa=orden.numero_mesa
        )

    detalle, created = DetallePedido.objects.get_or_create(
        pedido=pedido, producto=producto, defaults={"cantidad": cantidad}
    )

    if not created:
        detalle.cantidad += cantidad

    detalle.save()
    pedido.actualizar_precio_total()

    return JsonResponse(
        {"success": True, "message": "Producto agregado correctamente."}
    )


def carrito_contenido(request):
    orden_pk = request.session.get("orden_pk")
    if not orden_pk:
        return HttpResponse("")

    pedido = (
        Pedido.objects.filter(
            orden_id=orden_pk, estado__in=["confirmacion", "preparacion"]
        )
        .order_by("-created_at")
        .first()
    )

    total_items = pedido.detalles.count() if pedido else 0

    html = render_to_string(
        "menu/partials/_carrito_contenido.html",
        {"pedido": pedido, "total_items": total_items},
        request=request,
    )

    return HttpResponse(html)


@require_POST
def confirmar_pedido(request):
    orden_pk = request.session.get("orden_pk")
    if not orden_pk:
        return JsonResponse({"success": False, "message": "Orden no encontrada."})

    pedido = Pedido.objects.filter(orden_id=orden_pk, estado="confirmacion").first()

    if not pedido or not pedido.detalles.exists():
        return JsonResponse({"success": False, "message": "El carrito está vacío."})

    pedido.estado = "preparacion"
    pedido.save()

    # ✅ Recargar el HTML actualizado del carrito
    total_items = pedido.detalles.count()

    html = render_to_string(
        "menu/partials/_carrito_contenido.html",
        {"pedido": pedido, "total_items": total_items},
        request=request,
    )

    return HttpResponse(html)


@require_POST
def actualizar_detalle_pedido(request, detalle_id):
    from .models import DetallePedido  # si no está ya importado

    detalle = (
        DetallePedido.objects.select_related("pedido", "producto")
        .filter(id=detalle_id)
        .first()
    )

    cantidad = int(request.POST.get("cantidad", 1))
    if not detalle or cantidad < 1:
        return HttpResponse(status=400)

    detalle.cantidad = cantidad
    detalle.save()
    detalle.pedido.actualizar_precio_total()

    html = render_to_string(
        "menu/partials/_carrito_item.html", {"item": detalle}, request=request
    )

    response = HttpResponse(html)
    response["HX-Trigger"] = "item-updated"
    return response


@require_POST
def eliminar_detalle_pedido(request, detalle_id):
    from .models import DetallePedido  # si no está ya importado

    detalle = (
        DetallePedido.objects.select_related("pedido").filter(id=detalle_id).first()
    )
    if not detalle:
        return HttpResponse(status=400)

    pedido = detalle.pedido
    detalle.delete()
    pedido.actualizar_precio_total()

    response = HttpResponse()
    response["HX-Trigger"] = "item-updated"
    return response


def ubicacion(request):
    return render(
        request,
        "menu/ubicacion.html",
        {
            "page_title": "Ubicación",
            "show_other_options": True,
            "show_footer": True,
        },
    )


def conocenos(request):
    return render(
        request,
        "menu/conocenos.html",
        {
            "page_title": "Conócenos",
            "show_other_options": True,
            "show_footer": True,
        },
    )
