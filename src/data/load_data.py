import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from src.utils.helpers import load_config

def download_dataset_if_needed(dataset_name, file_name, save_path):
    """
    Descarga un archivo csv de un dataset de Kaggle si no existe localmente.

    Crea el directorio de guardado si no existe. Autentica la API de Kaggle
    y descarga el archivo solicitado.

    :param dataset_name: Nombre del dataset en Kaggle (e.g. 'mexwell/smart-home-energy-consumption').
    :type dataset_name: str
    :param file_name: Nombre del archivo a descargar dentro del dataset.
    :type file_name: str
    :param save_path: Ruta local donde se guardará el archivo descargado.
    :type save_path: str
    :return: Ruta completa al archivo descargado o existente.
    :rtype: str
    """
    os.makedirs(save_path, exist_ok=True)
    full_path = os.path.join(save_path, file_name)

    if not os.path.exists(full_path):
        print(f"Archivo no encontrado. Descargando {file_name} desde Kaggle...")
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_file(dataset_name, file_name, path=save_path, force=False, quiet=False)
    return full_path

def load_raw_data(config):
    """
    Carga los datos en un DataFrame de pandas descargando el archivo si es necesario.

    Extrae la información relevante del diccionario de configuración y llama
    a la función para descargar el dataset si no está disponible localmente.

    :param config: Diccionario con la configuración, debe contener las claves:
                   - 'data': con 'kaggle_dataset' y 'file_name'
                   - 'paths': con 'raw_data' para el path de guardado
    :type config: dict
    :return: DataFrame con los datos cargados desde CSV.
    :rtype: pandas.DataFrame
    """
    dataset_name = config["data"]["kaggle_dataset"]
    file_name = config["data"]["file_name"]
    save_path = config["paths"]["raw_data"]

    file_path = str(download_dataset_if_needed(dataset_name, file_name, save_path))
    return pd.read_csv(file_path)

if __name__ == '__main__':
    config = load_config()
    df = load_raw_data(config)
    print(df.head())