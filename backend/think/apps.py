from django.apps import AppConfig


class ThinkConfig(AppConfig):
    """
    Subclass of AppConfig representing the configuration for the 'think' app.

    Attributes:
        default_auto_field (str): The default auto field to use for models in this app.
        name (str): The name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.think'
