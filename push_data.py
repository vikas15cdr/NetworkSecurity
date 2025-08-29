import os
import sys
import json
from dotenv import load_dotenv
import certifi   ## python package that provide set or root certificates for validating the trustworthiness of SSL certificates and make secure http connection
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGODB_URI = os.getenv("MONGO_URI")

ca = certifi.where() ## get the path of the certificate bundle (ca is certificate authority)

class NetworkDataExtract():


    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def csv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values()) ## convert dataframe to list of json data
            return records
        except Exception as e:
            logging.error(f"Error occurred while converting CSV to JSON: {e}")
            raise NetworkSecurityException(e, sys) from e

    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))

        except Exception as e:
            logging.error(f"Error occurred while inserting data to MongoDB: {e}")
            raise NetworkSecurityException(e, sys) from e
        

if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE_NAME = "VIKAS15ML"
    COLLECTION_NAME = "Network_Data"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(f"Total {len(records)} records found in csv file")
    logging.info(f"ETL process started")
    logging.info(f"Total {len(records)} records found in csv file")
    no_of_records = networkobj.insert_data_mongodb(records, database=DATABASE_NAME, collection=COLLECTION_NAME)
    print(f"Total {no_of_records} records inserted to MongoDB database {DATABASE_NAME} and collection name is {COLLECTION_NAME}")
    logging.info(f"Total {no_of_records} records inserted to MongoDB database {DATABASE_NAME} and collection name is {COLLECTION_NAME}")
