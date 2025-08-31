from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e)

    def validate_no_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config.get("columns", []))
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            logging.error(f"Error occurred during column validation: {e}")
            raise NetworkSecurityException(e,sys)

    def validate_numerical_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            numerical_columns = self._schema_config.get("numerical_columns", [])
            dataframe_columns = dataframe.columns
            
            missing_numerical_columns = [col for col in numerical_columns if col not in dataframe_columns]
            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
                return False

            return True
        except Exception as e:
            logging.error(f"Error occurred during numerical column validation: {e}")
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True 
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)

                # If p-value is less than threshold, distributions are different (drift found)
                if threshold > is_same_dist.pvalue:
                    is_found = True
                    status = False # Set status to False as drift is found
                else:
                    is_found = False
                
                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            
            return status
        except Exception as e:
            logging.error(f"Error occurred during dataset drift detection: {e}")
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.training_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path

            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            
            is_valid = True

            # Validate number of columns
            if not self.validate_no_of_columns(dataframe=train_df):
                is_valid = False
                error_message += "Train dataframe has an invalid number of columns.\n"
            if not self.validate_no_of_columns(dataframe=test_df):
                is_valid = False
                error_message += "Test dataframe has an invalid number of columns.\n"

            # Validate numerical columns
            if not self.validate_numerical_columns(dataframe=train_df):
                is_valid = False
                error_message += "Train dataframe has invalid numerical columns.\n"
            if not self.validate_numerical_columns(dataframe=test_df):
                is_valid = False
                error_message += "Test dataframe has invalid numerical columns.\n"

            if not is_valid:
                logging.error(f"Data validation errors found:\n{error_message}")
                raise NetworkSecurityException(error_message)

            # Validate dataset drift
            drift_status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            if not drift_status:
                logging.warning("Dataset drift detected between train and test sets.")
            
            # Save the validated dataframes
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)

            data_validation_artifact = DataValidationArtifact(
                validation_status=is_valid, 
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            logging.error(f"Error occurred during data validation: {e}")
            raise NetworkSecurityException(e, sys) from e