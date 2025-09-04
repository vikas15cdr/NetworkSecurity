import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import pandas as pd
import numpy as np
import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        logging.error(f"Error reading YAML file at {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e

def write_yaml_file(file_path: str, content: object,replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        logging.error(f"Error writing YAML file at {file_path}: {e}")
        raise NetworkSecurityException(e,sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        logging.error(f"Error saving numpy array data at {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info(f"Entered save_object with file_path: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Exited save_object with file_path: {file_path}")
    except Exception as e:
        logging.error(f"Error saving object at {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e