import json
import os


class ThinkModelFactory:
    """
    This class provides a static method `create_model` that creates a model instance based on a given configuration
    name.
    """
    @staticmethod
    def create_model(config_name):
        file_path = os.path.join(os.path.dirname(__file__), '../config/think/' + config_name + '.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        provider = config.get('provider')
        model = config.get('model')
        rag_function = config.get('rag_function')
        prompt_start = config.get('prompt_start', '')
        prompt_end = config.get('prompt_end', '')
        context_start = config.get('context_start', '')
        context_end = config.get('context_end', '')

        if not provider or not model:
            raise ValueError("The configuration file must specify both 'provider' and 'model'.")

        return {
            'provider': provider,
            'model': model,
            'rag_function': rag_function,
            'prompt_start': prompt_start,
            'prompt_end': prompt_end,
            'context_start': context_start,
            'context_end': context_end,
        }
