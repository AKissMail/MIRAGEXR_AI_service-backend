from django.apps import AppConfig


class OptionsConfig(AppConfig):
    """
    A class that represents the configuration options for the 'options' app in Django.

    Attributes:
        default_auto_field (str): The default auto field to use for model's primary key.
            It is set to 'django.db.models.BigAutoField' by default.
        name (str): The name of the app, which is set to 'options'.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'options'
