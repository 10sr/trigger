import django.apps


class AppConfig(django.apps.AppConfig):  # type: ignore   # disallow_subclassing_any
    name = "proj.manageproj"
    lavel = "manageproj"
