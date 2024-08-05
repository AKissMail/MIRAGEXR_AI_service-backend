from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    This class defines the configuration for the authentication app.

    Attributes:
        default_auto_field (str): The default auto field for models in the authentication app.
        name (str): The name of the authentication app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
