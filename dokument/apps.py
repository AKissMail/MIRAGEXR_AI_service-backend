from django.apps import AppConfig


class DokumentApp(AppConfig):
    """
    DokumentApp

    AppConfig class for the 'dokument' app.

    Attributes:
        default_auto_field (str): The default auto field for the app.
        name (str): The name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dokument'
