from django.apps import AppConfig


class SpeakConfig(AppConfig):
    """Configuration class for the Speak app.

    Inherits from `AppConfig` and provides additional configuration options specific to the Speak app.

    Attributes:
        default_auto_field (str): The default auto field to use for models in the Speak app.
        name (str): The name of the Speak app.

    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "speak"
