# from django.contrib import admin
import core.views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(
        "login/",
        core.views.LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
    path("logout/", core.views.LogoutView.as_view(), name="logout"),
    path("admin_panel/", include("admin_panel.urls", namespace="admin_panel")),
    path("", include("menu.urls", namespace="menu")),
    path("kitchen/", include("kitchen_panel.urls", namespace="kitchen")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
