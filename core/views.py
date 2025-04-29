from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.template import loader


class CustomLoginView(LoginView):
    template_name = "login/login.html"


def robots_txt(request):
    lines = loader.render_to_string("robots.txt")
    return HttpResponse(lines, content_type="text/plain")
