import yaml
import os

CONFIG_PATH = "config/config.yaml"

def load_config(path=CONFIG_PATH):
    """
    Carga la configuración desde un archivo YAML.

    :param path: Ruta al archivo de configuración YAML. Por defecto, 'config/config.yaml'.
    :type path: str
    :return: Diccionario con la configuración cargada.
    :rtype: dict
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)