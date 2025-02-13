from django.urls import reverse as _reverse


def reverse(view_name: str, *args, urlconf=None, current_app=None, **kwargs):
    """
    Extend the built-in Django reverse function.

    It extends the original Django `reverse` function by allowing the use of positional
    arguments (*args) along with keyword arguments (**kwargs)
    """
    return _reverse(
        view_name,
        urlconf=urlconf,
        current_app=current_app,
        args=args,
        kwargs=kwargs,
    )
