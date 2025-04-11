from .models import RestauranteInfo


def info_restaurante(request):
    info, _ = RestauranteInfo.objects.get_or_create(id=1)
    return {"info_restaurante": info}
