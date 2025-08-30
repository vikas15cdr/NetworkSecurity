from networksecurity.components.data_ingestion import DataIngestion
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiating data ingestion process.")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info("Data ingestion process completed successfully.")
    except Exception as e:
        logging.error(f"Error occurred in main script: {e}")
        raise NetworkSecurityException(e, sys) from e