from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.entity.config_entity import DataIngestionConfig
import sys, os
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

class DataIngestion:

    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(f"Error occurred while initializing DataIngestion: {e}")
            raise NetworkSecurityException(e, sys) from e
    
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_URI)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace(to_replace="na", value=np.nan, inplace=True)
            logging.info(f"Exported collection {collection_name} from database {database_name} as dataframe.")
            return df
        
        except Exception as e:
            logging.error(f"Error occurred while exporting collection as dataframe: {e}")
            raise NetworkSecurityException(e, sys) from e
        
    def export_data_to_feature_store(self, df: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Exported data to feature store at {feature_store_file_path}.")
            return df
        except Exception as e:
            logging.error(f"Error occurred while exporting data to feature store: {e}")
            raise NetworkSecurityException(e, sys) from e

    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            train_set,test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train-test split on dataframe.")
            logging.info(f"Train set shape: {train_set.shape}, Test set shape: {test_set.shape}")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info(f"Exported train data to {self.data_ingestion_config.training_file_path}.")
            logging.info(f"Exported test data to {self.data_ingestion_config.testing_file_path}.")

        except Exception as e:
            logging.error(f"Error occurred while splitting data into train and test sets: {e}")
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            dataframe= self.export_collection_as_dataframe()
            dataframe= self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            dataingestionartifact = DataIngestionArtifact(training_file_path=self.data_ingestion_config.training_file_path,
                                                        testing_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            logging.error(f"Error occurred while initiating data ingestion: {e}")
            raise NetworkSecurityException(e, sys) from e