from django.apps import AppConfig
import fasttext


class ThinkConfig(AppConfig):
    """
    Subclass of AppConfig representing the configuration for the 'think' app.

    Attributes:
        default_auto_field (str): The default auto field to use for models in this app.
        name (str): The name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'think'
    ft_model = None

    def ready(self):
        self.ft_model = fasttext.load_model('./cc.no.300.bin')
