from django import template
from django.forms import Form

register = template.Library()


@register.inclusion_tag("common/forms/_non_field_errors.html")
def non_field_errors(form: Form) -> dict[str, Form]:
    """Render a standard form's non-fields-errors list."""
    return {"form": form}
