from django.shortcuts import render, get_object_or_404, redirect
from admin_panel.models import Producto
from .models import Pedido, DetallePedido
from django.db.models import Sum
from django.http import JsonResponse


# Create your views here.
def Menu_Productos(request):
    numero_mesa = request.session.get('numero_mesa', None)

    # Si se cambia de mesa, limpiar el carrito si no hay pedido activo
    if numero_mesa:
        pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()
        if not pedido:  # Si no hay pedido, se reinicia el carrito
            request.session['carrito'] = {}
            request.session['carrito_total'] = 0

    producto = Producto.objects.all()
    return render(
        request, 'menu/menu_lista.html',
          {"show_sidebar": True,
           "producto": producto,
           "numero_mesa": numero_mesa})

# Vista para agregar productos al carrito
def agregar_al_carrito(request, producto_id, numero_mesa, cantidad):
    if request.method == "POST":
        # Guardar el número de mesa en la sesión
        if request.session.get('numero_mesa') != numero_mesa:
            request.session['numero_mesa'] = numero_mesa
            request.session['carrito'] = {}  # Limpiar carrito al cambiar de mesa

        producto = get_object_or_404(Producto, id=producto_id)

        pedido, created = Pedido.objects.get_or_create(
            numero_mesa=numero_mesa,
            estado='preparacion',
            defaults={'precio_total': 0}
        )

        detalle, created = DetallePedido.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={'cantidad': cantidad, 'precio_total': producto.precio * cantidad}
        )

        if not created:
            detalle.cantidad += cantidad
            detalle.precio_total = detalle.cantidad * producto.precio
            detalle.save()

        # Actualizar precio total del pedido
        pedido.precio_total = pedido.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
        pedido.save()

        # Actualizar total de productos en la sesión
        total_items = sum(d.cantidad for d in pedido.detalles.all())
        request.session['carrito_total'] = total_items

        return JsonResponse({"success": True, "total_items": total_items})

    return JsonResponse({"success": False}, status=400)
    
def modificar_carrito(request, producto_id, numero_mesa, cantidad):
    if request.method == "POST":
        pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()
        if not pedido:
            return JsonResponse({'error': 'No hay pedido en curso'}, status=400)

        detalle = DetallePedido.objects.filter(pedido=pedido, producto_id=producto_id).first()

        if detalle:
            if cantidad > 0:
                detalle.cantidad = cantidad
                detalle.precio_total = detalle.cantidad * detalle.producto.precio
                detalle.save()
            else:
                detalle.delete()  # Si la cantidad es 0, eliminar el producto

            # Actualizar el precio total del pedido
            pedido.precio_total = pedido.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
            pedido.save()

        return JsonResponse({'mensaje': 'Carrito actualizado', 'precio_total': pedido.precio_total})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def ver_carrito(request, numero_mesa):
    pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()
    detalles = pedido.detalles.all() if pedido else []
    return render(request, 'menu/carrito.html', {
        "show_sidebar": True,
        "pedido": pedido,
        "detalles": detalles
    })

def obtener_carrito_actual(request):
    numero_mesa = request.session.get('numero_mesa', None)  # Obtener el número de mesa de la sesión

    if numero_mesa:
        # Buscar el pedido correspondiente a esa mesa
        pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()

        if pedido:
            productos_en_carrito = DetallePedido.objects.filter(pedido=pedido).values_list('producto_id', flat=True)
            return JsonResponse({"productos": list(productos_en_carrito)})
    
    return JsonResponse({"productos": []})  # Si no hay carrito, devolver lista vacía

def quitar_del_carrito(request, producto_id):
    if request.method == "POST":
        numero_mesa = request.session.get('numero_mesa', None)
        if not numero_mesa:
            return JsonResponse({'error': 'No se ha seleccionado una mesa'}, status=400)

        pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()
        if not pedido:
            return JsonResponse({'error': 'No hay pedido en curso'}, status=400)

        detalle = DetallePedido.objects.filter(pedido=pedido, producto_id=producto_id).first()

        if detalle:
            if detalle.cantidad > 1:
                detalle.cantidad -= 1
                detalle.precio_total = detalle.cantidad * detalle.producto.precio
                detalle.save()
            else:
                detalle.delete()  # Si la cantidad es 1, eliminar el producto del carrito

            # Actualizar el precio total del pedido
            pedido.precio_total = pedido.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
            pedido.save()

        return JsonResponse({'mensaje': 'Producto actualizado', 'precio_total': pedido.precio_total})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def eliminar_del_carrito(request, producto_id):
    if request.method == "POST":
        numero_mesa = request.session.get('numero_mesa', None)
        if not numero_mesa:
            return JsonResponse({'error': 'No se ha seleccionado una mesa'}, status=400)

        pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()
        if not pedido:
            return JsonResponse({'error': 'No hay pedido en curso'}, status=400)

        DetallePedido.objects.filter(pedido=pedido, producto_id=producto_id).delete()

        # Actualizar el precio total del pedido
        pedido.precio_total = pedido.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
        pedido.save()

        return JsonResponse({'mensaje': 'Producto eliminado', 'precio_total': pedido.precio_total})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def marcar_pedido_entregado(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pedido.estado = "entregado"
    pedido.save()

    # Limpiar el carrito al entregar el pedido
    request.session['carrito'] = {}
    request.session['carrito_total'] = 0  # Reiniciar contador de productos
    request.session['numero_mesa'] = None  # Quitar la mesa de la sesión

    return JsonResponse({'mensaje': 'Pedido entregado y carrito reiniciado', 'carrito_total': 0})