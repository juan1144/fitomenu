from dataclasses import dataclass

from django import template
from django.apps import apps

register = template.Library()


@dataclass
class BreadCrumb:
    """Represents an individual breadcrumb item."""

    title: str
    url: str = None


@register.inclusion_tag("common/_breadcrumb.html", takes_context=True)
def breadcrumb(context) -> dict[str, list[BreadCrumb] | str]:
    """
    Generate the breadcrumb structure and renders the breadcrumb component.

    Returns [dict]:
            - first_item: Name of the app or namespace.
            - items: List of BreadCrumb objects (or None if not provided).
            - last_item: Page title for the current view.
    """
    app_name = ""
    namespace = context["request"].resolver_match.namespaces
    joined_namespace = ":".join(namespace)

    if joined_namespace != "core":
        app_name = str(apps.get_app_config(namespace[0]).verbose_name)

    items = context.get("breadcrumb", None)
    if isinstance(items, BreadCrumb):
        items = [items]

    page_title = context.get("page_title", "")
    return {"first_item": app_name, "items": items, "last_item": page_title}
