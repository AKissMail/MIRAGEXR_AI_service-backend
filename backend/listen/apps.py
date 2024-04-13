from django.apps import AppConfig


class ListenConfig(AppConfig):
    """
    Represents the configuration for the 'listen' Django app.

    Attributes:
    - default_auto_field (str): Specifies the default primary key type for models in the app.
    - name (str): The name of the 'listen' app.

    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "listen"
