import pymysql
from urllib.parse import quote_plus
import urllib
import logging.config
import logging.handlers
import json
import pandas as pd
from sqlalchemy import create_engine
import os
import warnings
import configparser
import requests
import paramiko

def setup_logging():
    try:
        # First attempt to configure logging
        logging.config.fileConfig('../parameters/logs.ini', disable_existing_loggers=False)
    except Exception:
        # If an exception occurs, try a different configuration
        logging.config.fileConfig('parameters/logs.ini', disable_existing_loggers=False)

    # Setting up the logger
    logger = logging.getLogger(__name__)

    # Configuring logging levels for various modules
    logging.getLogger("googleapiclient").setLevel(logging.WARNING)
    logging.getLogger('oauth2client').setLevel(logging.WARNING)
    logging.getLogger('google_auth_httplib2').setLevel(logging.WARNING)
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    return logger


class DatabaseConnection:
    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                self.config = json.load(config_file)

        except Exception as e:
            print(e)
            raise Exception(e)

        self.engine = None
        self.connection = None
        self.params = None
        self.logger = setup_logging()


    def Neutrino(self):

        try:
            self.params = urllib.parse.quote_plus(f'DRIVER={self.config["Neutrino"]["driver"]};'
                                                  f'Server={self.config["Neutrino"]["server"]};'
                                                  f'Database={self.config["Neutrino"]["database"]};'
                                                  f'UID={self.config["Neutrino"]["username"]};'
                                                  f'PWD={self.config["Neutrino"]["password"]};')



            # Establish the engine
            self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.params)
            self.connection = self.engine.connect()
            self.logger.info("Database connection established---------------------------")

        except OSError as e:
            self.logger.info(e)
            self.logger.info("Connection - FAILED")


    def close(self):
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        self.logger.info("Connection closed----------------------------------------------")

    # Simple Extract data
    def extract_data(self, query: str) -> pd.DataFrame:
        try:
            if self.connection is None:
                raise Exception("No Connection found")
            data = pd.read_sql_query(query, con=self.connection)
            # logger.info(str(len(data)) + " " + "Rows of Data Extracted")
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)
        return data

    # Import data
    def insert_data(self, data_frame: pd.DataFrame, table_name: str):
        try:
            data_frame.to_sql(name=table_name, con=self.engine, if_exists='append', method='multi', chunksize=50,
                              index=False)
            self.logger.info(str(len(data_frame)) + " " + "Rows of Data Imported")
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)


    # Extract data based on multiple parameters
    def extract_data_mp(self, query: str, stime, etime) -> pd.DataFrame:
        try:
            if self.connection is None:
                raise Exception("No Connection found")
            data = pd.read_sql_query(query, con=self.connection, params=[stime, etime])
            # logger.info(str(len(data)) + " " + "Rows of Data Extracted")
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)
        return data

    # Extract data based on single parameter
    def extract_data_sp(self, query: str, x) -> pd.DataFrame:
        try:
            if self.connection is None:
                raise Exception("No Connection found")
            data = pd.read_sql_query(query, con=self.connection, params=[x])
            # logger.info(str(len(data)) + " " + "Rows of Data Extracted")
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)
        return data
