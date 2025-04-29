# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(
        "login/",
        LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin_panel/", include("admin_panel.urls", namespace="admin_panel")),
    path("", include("menu.urls", namespace="menu")),
    path("kitchen/", include("kitchen_panel.urls", namespace="kitchen")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
