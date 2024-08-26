from django.template import Library

register = Library()


@register.filter()
def current_path(path, menu):
    return path.endswith(f"/{menu}")
