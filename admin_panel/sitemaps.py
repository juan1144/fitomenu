from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ["menu_lista", "conocenos", "ubicacion"]

    def location(self, item):
        return reverse(item)
