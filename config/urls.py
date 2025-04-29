from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from admin_panel.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

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
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
