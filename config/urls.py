# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("admin_panel/", include("admin_panel.urls", namespace="admin_panel")),
    path("", include("menu.urls", namespace="menu")),
    path("kitchen/", include("kitchen_panel.urls", namespace="kitchen")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
