import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from networksecurity.utils.main_utils.utils import load_object, save_object, load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import evaluate_models

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)
import mlflow

import dagshub
dagshub.init(repo_owner='vikas1969awz', repo_name='NetworkSecurity', mlflow=True)


class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            logging.error(f"Error occurred during Model Trainer initialization: {e}")
            raise NetworkSecurityException(e, sys) from e

    def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score
            accuracy_score = classification_metric.accuracy_score

            mlflow.log_metric("F1_Score", f1_score)
            mlflow.log_metric("Precision_Score", precision_score)
            mlflow.log_metric("Recall_Score", recall_score)
            mlflow.log_metric("Accuracy_Score", accuracy_score)

    def train_model(self, x_train, y_train, x_test, y_test):
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
            model_report: dict = evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test,
                                            models=models, params=params)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            train_score = best_model.score(x_train, y_train)
            test_score = best_model.score(x_test, y_test)
            logging.info(f"Best model found: {best_model_name}")
            logging.info(f"Best model train score: {train_score}")
            logging.info(f"Best model test score: {test_score}")

            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            logging.info(f"Training classification metrics: {classification_train_metric}")

            ## track metrics using mlflow
            self.track_mlflow(best_model,classification_train_metric)

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            logging.info(f"Testing classification metrics: {classification_test_metric}")

            ## track metrics using mlflow
            self.track_mlflow(best_model,classification_test_metric)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

            save_object("final_model/model.pkl", best_model)

            Model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                train_metric_artifact = classification_train_metric,
                test_metric_artifact = classification_test_metric,
            )
            logging.info(f"Model Trainer Artifact: {Model_trainer_artifact}")
            return Model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Loading transformed training and testing data")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)
            logging.info("Splitting input and target features")

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            logging.error(f"Error occurred during model training: {e}")
            raise NetworkSecurityException(e, sys) from e

