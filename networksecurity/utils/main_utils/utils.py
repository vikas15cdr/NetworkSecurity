import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import pandas as pd
import numpy as np
import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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

def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        logging.error(f"Error loading object from {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        logging.error(f"Error loading numpy array data from {file_path}: {e}")
        raise NetworkSecurityException(e, sys) from e

def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        logging.error(f"Error evaluating models: {e}")
        raise NetworkSecurityException(e, sys) from e