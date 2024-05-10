from django.apps import AppConfig


class DocumentApp(AppConfig):
    """
    DocumentApp

    AppConfig class for the 'document' app.

    Attributes:
        default_auto_field (str): The default auto field for the app.
        name (str): The name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'document'
