from django.urls import path
from .views import kitchen_panel, kitchen_orders, update_order_status
app_name = "kitchen"

urlpatterns = [
    path("", kitchen_panel, name="kitchen_panel"),
    path("orders/", kitchen_orders, name="kitchen_orders"),
    path("orders/<int:pedido_id>/update/", update_order_status, name="update_order_status"),
]
