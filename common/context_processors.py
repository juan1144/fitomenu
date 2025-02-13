from dataclasses import dataclass, field
from typing import Any

from django.http import HttpRequest
from common.http_utils import reverse  # Asegurar que esta función está disponible

MAIN_NAMESPACE = "core"


@dataclass
class SubMenu:
    """
    Represents an individual submenu item within a sidebar menu.

    Each submenu item contains information about its title and the view it links to.
    """

    title: str
    view_name: str
    view_kwargs: dict[str, Any] = field(default_factory=dict)
    url: str = None
    is_active: bool = False

    def __post_init__(self):
        """Automatically resolves the URL using `view_name` and `view_kwargs`."""
        self.url = reverse(self.view_name, **self.view_kwargs)

    def check_is_active(self, namespace: str) -> None:
        """Set the submenu as active if the current namespace matches its view."""
        if namespace == MAIN_NAMESPACE:
            self.is_active = True
        else:
            namespace = ":".join(namespace.split(":")[:2])
            self.is_active = self.view_name.startswith(namespace)


@dataclass
class Menu:
    """
    Represents a sidebar menu containing multiple submenus.

    The class dynamically determines if the menu should be displayed and
    if it is currently active based on the current user context.
    """

    title: str
    request: HttpRequest
    submenus: list[SubMenu]
    is_active: bool = False

    def __post_init__(self):
        """Initialize the menu by evaluating active states."""
        namespace = ":".join(self.request.resolver_match.namespaces)
        for submenu in self.submenus:
            submenu.check_is_active(namespace)
            self.is_active = self.is_active or submenu.is_active


def sidebar(request) -> dict:
    """Automatically sets the `is_active` attributes for menus."""
    return {
        "menus": [
            Menu(
                title="Inicio",
                request=request,
                submenus=[
                    SubMenu(
                        title="Página principal",
                        view_name="admin_panel:lista_productos",
                    ),
                ],
            ),
        ],
    }
