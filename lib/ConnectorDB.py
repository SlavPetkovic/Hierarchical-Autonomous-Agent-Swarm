#-----------------------------------------------------------------------------------
# Connector class to AzureSQL
#-----------------------------------------------------------------------------------

# Importing necessary libraries
from urllib.parse import quote_plus
import urllib
import logging.config
import logging.handlers
import json
import pandas as pd
from sqlalchemy import create_engine

# Function to setup logging configuration
def setup_logging():
    try:
        # Configuring logging using a file located at '../parameters/logs.ini'
        logging.config.fileConfig('../parameters/logs.ini', disable_existing_loggers=False)
    except Exception:
        # In case of an exception, try a different path for the logging configuration file
        logging.config.fileConfig('parameters/logs.ini', disable_existing_loggers=False)

    # Initialize and return a logger object
    logger = logging.getLogger(__name__)

    # Set logging levels for specific libraries to reduce verbosity
    logging.getLogger("googleapiclient").setLevel(logging.WARNING)
    logging.getLogger('oauth2client').setLevel(logging.WARNING)
    logging.getLogger('google_auth_httplib2').setLevel(logging.WARNING)
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    return logger

# Class to handle database connections
class DBConnection:
    # Constructor method
    def __init__(self, config_file_path):
        self.config = self.load_config(config_file_path)
        self.engine = None
        self.connection = None
        self.params = None
        self.logger = setup_logging()

    # Method to load configuration from a file
    def load_config(self, config_file_path):
        try:
            # Opening and loading the configuration file
            with open(config_file_path) as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            # Log and raise an error if the config file is not found
            self.logger.error("Config file not found")
            raise
        except json.JSONDecodeError:
            # Log and raise an error if there is a JSON decoding issue
            self.logger.error("Error decoding JSON from config file")
            raise

    # Method to establish a database connection
    def neutrino(self):
        self.logger.info("Database connection attempt---------------------------")
        try:
            # Constructing the database connection parameters from the configuration
            self.params = urllib.parse.quote_plus(
                f'DRIVER={self.config["Neutrino"]["driver"]};'
                f'SERVER={self.config["Neutrino"]["server"]};'
                f'DATABASE={self.config["Neutrino"]["database"]};'
                f'UID={self.config["Neutrino"]["username"]};'
                f'PWD={self.config["Neutrino"]["password"]};'
                f'ENCRYPT={self.config["Neutrino"]["encrypt"]};'
                f'TRUSTSERVERCERTIFICATE={self.config["Neutrino"]["trust_server_certificate"]};'
                f'CONNECTION TIMEOUT={self.config["Neutrino"]["connection_timeout"]};'
            )

            # Establishing the database connection using SQLAlchemy
            self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.params}")
            self.connection = self.engine.connect()
            self.logger.info("Database connection established---------------------------")
            return self.engine
        except Exception as e:
            # Log and raise an error if there is a connection issue
            self.logger.error(f"Database connection error: {e}")
            raise

    # Method to close the database connection
    def close(self):
        # Close the connection and dispose the engine if they exist
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        self.logger.info("Connection closed----------------------------------------------")

    # Method to extract data from the database
    def extract_data(self, query: str) -> pd.DataFrame:
        try:
            if self.connection is None:
                # Raise an exception if no database connection is found
                raise Exception("No Connection found")
            # Execute the query and store the result in a DataFrame
            data = pd.read_sql_query(query, con=self.connection)
            self.logger.info(str(len(data)) + " " + "Rows of Data Extracted")
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)
        return data

    # Method to insert data into the database
    def insert_data(self, data_frame: pd.DataFrame, table_name: str):
        try:
            # Inserting data into the specified table
            data_frame.to_sql(name=table_name, con=self.engine, if_exists='append', method='multi', chunksize=50,
                              index=False)
            self.logger.info(str(len(data_frame)) + " " + "Rows of Data Imported")
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)

    # Method to extract data with multiple parameters
    def extract_data_mp(self, query: str, stime, etime) -> pd.DataFrame:
        try:
            if self.connection is None:
                # Raise an exception if no database connection is found
                raise Exception("No Connection found")
            # Execute the query with parameters and store the result in a DataFrame
            data = pd.read_sql_query(query, con=self.connection, params=[stime, etime])
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)
        return data

    # Method to extract data with a single parameter
    def extract_data_sp(self, query: str, x) -> pd.DataFrame:
        try:
            if self.connection is None:
                # Raise an exception if no database connection is found
                raise Exception("No Connection found")
            # Execute the query with a parameter and store the result in a DataFrame
            data = pd.read_sql_query(query, con=self.connection, params=[x])
        except Exception as e:
            self.logger.info(e)
            raise Exception(e)
        return data
