import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from menu.models import Pedido

@require_GET
def kitchen_orders(request):
    pedidos = Pedido.objects.filter(estado='preparacion').order_by('created_at')

    data = [
        {
            "id": pedido.id,
            "numero_mesa": pedido.numero_mesa,
            "estado": pedido.estado,
            "precio_total": pedido.precio_total,
            "notas": pedido.notas,
            "created_at": pedido.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "detalles": [
                {
                    "producto": item.producto.nombre,
                    "cantidad": item.cantidad,
                    "precio_total": float(item.precio_total),
                }
                for item in pedido.detalles.all()
            ]
        }
        for pedido in pedidos
    ]
    return JsonResponse({"pedidos": data})

@csrf_exempt
@require_POST
def update_order_status(request, pedido_id):
    print(f"Llamando a update_order_status con pedido_id: {pedido_id}")

    pedido = get_object_or_404(Pedido, id=pedido_id)

    try:
        body = json.loads(request.body)
        nuevo_estado = body.get("estado")

        print(f"Recibido estado: {nuevo_estado}")

        if nuevo_estado not in ["entregado", "cancelado"]:
            return JsonResponse({"error": "Estado inválido"}, status=400)

        pedido.estado = nuevo_estado
        pedido.save()

        print(f"Pedido {pedido_id} actualizado a {nuevo_estado}")

        return JsonResponse({"mensaje": f"Pedido {pedido.id} actualizado a {nuevo_estado}"})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido"}, status=400)

def kitchen_panel(request):
    return render(request, "kitchen_panel/panel.html",
                  {"page_title": "Panel de Cocina", "show_sidebar": False})
