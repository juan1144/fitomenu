from django.urls import path
from .views import robots_txt

urlpatterns = [
    # path("login/", CustomLoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    path("robots.txt", robots_txt, name="robots.txt"),
]
