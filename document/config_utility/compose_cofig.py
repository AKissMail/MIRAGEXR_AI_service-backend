import json
import os

from django.conf import settings


def load_static_configs():
    config_dir = os.path.join(settings.BASE_DIR, 'config')
    static_configs = []

    for subdir in ['listen', 'speak', 'think']:
        base_config_path = os.path.join(config_dir, subdir, 'baseConfig.json')
        with open(base_config_path, 'r') as file:
            static_configs.extend(json.load(file))

    return static_configs


def load_dynamic_configs():
    dynamic_config_dir = os.path.join(settings.BASE_DIR, 'config', 'think')
    dynamic_configs = []

    for filename in os.listdir(dynamic_config_dir):
        if filename.endswith('.json') and filename != 'baseConfig.json':
            with open(os.path.join(dynamic_config_dir, filename), 'r') as file:
                dynamic_config = json.load(file)

                transformed_config = {
                    "endpointName": "think/",
                    "name": dynamic_config.get("name", "Default Name"),
                    "description": dynamic_config.get("description", "Default Description"),
                    "apiName": dynamic_config["apiName"]
                }
                dynamic_configs.append(transformed_config)

    return dynamic_configs


def update_options_json():
    static_configs = load_static_configs()
    dynamic_configs = load_dynamic_configs()

    all_configs = static_configs + dynamic_configs

    options_json_path = os.path.join(settings.BASE_DIR, 'config', 'options.json')
    with open(options_json_path, 'w') as file:
        json.dump(all_configs, file, indent=4)
