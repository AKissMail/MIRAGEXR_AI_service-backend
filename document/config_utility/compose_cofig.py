import json
import os

from django.conf import settings


def load_static_configs():
    """
    Load Static Configs

    Load static configurations from the 'config' directory. This method reads three subdirectories: 'listen', 'speak',
    and 'think', and reads the 'baseConfig.json' file from each subdirectory. It then aggregates the configurations
    from all three subdirectories and returns them as a list.

    Returns:
        List: A list of static configurations.

    """
    config_dir = os.path.join(settings.BASE_DIR, 'config')
    static_configs = []

    for subdir in ['listen', 'speak', 'think']:
        base_config_path = os.path.join(config_dir, subdir, 'baseConfig.json')
        with open(base_config_path, 'r') as file:
            static_configs.extend(json.load(file))

    return static_configs


def load_dynamic_configs():
    """

    Function: load_dynamic_configs

    Description:
    This function loads dynamic configurations from JSON files located in the 'config/think' directory.
    It reads each JSON file, transforms the data, and adds it to a list of dynamic configurations.
    The list of transformed configurations is then returned.

    Parameters:
    None

    Returns:
    dynamic_configs (list): A list of dictionaries representing the transformed dynamic configurations.
    Each dictionary contains the following keys:
    - "endpointName": A string representing the endpoint name.
    - "name": A string representing the name of the dynamic configuration. Defaults to "Default Name" if not specified.
    - "description": A string representing the description of the dynamic configuration. Defaults to "Default
    Description" if not specified.
    - "apiName": A string representing the API name of the dynamic configuration.

    """
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
    """
    Update options.json file with the latest configurations.

    This method combines static and dynamic configurations, and updates the options.json file with the new
    configurations. The options.json file is located in the 'config' directory of the project.

    Returns:
        None

    Example Usage:
        update_options_json()
    """
    static_configs = load_static_configs()
    dynamic_configs = load_dynamic_configs()

    all_configs = static_configs + dynamic_configs

    options_json_path = os.path.join(settings.BASE_DIR, 'config', 'options.json')
    with open(options_json_path, 'w') as file:
        json.dump(all_configs, file, indent=4)
