from django.shortcuts import render, get_object_or_404, redirect
from admin_panel.models import Producto
from .models import Pedido, DetallePedido
from django.db.models import Sum
from django.http import JsonResponse


# Create your views here.
def Menu_Productos(request):
    producto = Producto.objects.all()
    numero_mesa = request.session.get('numero_mesa', None)  # Obtener el número de mesa de la sesión
    return render(
        request, 'menu/menu_lista.html',
          {"show_sidebar": False,
           "producto":producto,
           "numero_mesa": numero_mesa})

# Vista para agregar productos al carrito
def agregar_al_carrito(request, producto_id, numero_mesa, cantidad):
    if request.method == "POST":

        # Guardamos el número de mesa en la sesión
        request.session['numero_mesa'] = numero_mesa

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

        # Actualizar el precio total del pedido
        pedido.precio_total = pedido.detalles.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
        pedido.save()

        total_items = sum(d.cantidad for d in pedido.detalles.all())

        return JsonResponse({"success": True, "total_items": total_items})

    return JsonResponse({"success": False}, status=400)

def ver_carrito(request, numero_mesa):
    pedido = Pedido.objects.filter(numero_mesa=numero_mesa, estado='preparacion').first()
    detalles = pedido.detalles.all() if pedido else []
    return render(request, 'menu/carrito.html', {
        "show_sidebar": True,
        "pedido": pedido,
        "detalles": detalles
    })
