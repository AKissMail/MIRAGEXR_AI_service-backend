from django.apps import AppConfig
import fasttext
import warnings


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
        self.load_fasttext_model()

    def load_fasttext_model(self):
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=UserWarning,
                                        message='`load_model` does not return WordVectorModel or SupervisedModel any '
                                                'more, but a `FastText` object which is very similar.')
                self.ft_model = fasttext.load_model('./cc.no.300.bin')
            print("FastText model loaded successfully.")
        except Exception as e:
            print(f"Error loading FastText model: {e}")