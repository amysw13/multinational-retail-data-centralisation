import os
import re
import yaml
import pandas as pd
import tabula
import requests
import boto3
from sqlalchemy.engine import Engine

class DataExtractor:
    ''' 
    DataExtractor - a class for extracting data from multiple data sources.
    =======================================================================

    DataExtractor, contains methods for retrieving and extracting data from AWS RDS 
    and S3 buckets, .pdf, .csv files, and web APIs. 
    Extracted data returned as pandas data frames. 
    '''
    def read_rds_table(self, table : str, engine : Engine):
        '''
        This function is used to read and download from AWS RDS or local database. This function
        is linked to the list_db_tables( ) function from DatabaseConnector Class.
        Reads the sql table and returns pandas dataframe object.
        
        Args:
            table (str): the name of table to retrieve data from.
            engine (Engine): name of the engine created to connect to the AWS RDS or local database.

        Returns:
            df (pd.DataFrame): returns sql table as a pandas dataframe object.
        '''
        user_df = pd.read_sql_table(f"{table}", engine)
        return user_df
    
    def retrieve_pdf_data(self):
        '''
        This function is used to read and extract data from .pdf files. 

        Returns:
            df (pd.DataFrame): returns concatenated list of df from pdf as a pandas dataframe object.
        '''
        pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        card_details_df = tabula.read_pdf(pdf_path, pages= 'all')
        card_details_df = pd.concat(card_details_df) #join list of df into a pandas dataframe
        return card_details_df
    
    def list_number_of_stores(self, endpoint : str):
        '''
        This function is used to find the number of stores listed on the web API. 
        A 'api_configuration.yaml' file needs to be accessible from Credentials,
        that stores a dictionary of the API access key and value.

        Args:
            endpoint (str): the url of the web API endpoint to retrieve number of stores.

        Returns:
            Number of stores (int): returns the response of the web api request as a integer. 
        '''
        with open('Credentials/api_configuration.yaml', 'r') as f:
            header = yaml.safe_load(f)
        response = requests.get(f"{endpoint}", headers=header)
        Num_of_stores = response.json()
        return Num_of_stores

    def retrieve_stores_data(self, Num_of_stores : dict, endpoint : str):
        '''
        This function is used to retrieve store data from web API, 
        by iterating through all stores by number of stores. 
        A 'api_configuration.yaml' file needs to be accessible from Credentials,
        that stores a dictionary of the API access key and value.

        Args:
            Num_of_stores (dict): Dictionary of response list_number_of_stores(), with value of number of stores data to download from web API.
            endpoint (str): the url of the web API endpoint to retrieve stores data.
    
        Returns:
            df (pd.DataFrame): returns the response of the web API requests as a pandas data frame.
        '''
        with open('Credentials/api_configuration.yaml', 'r') as f:
            header = yaml.safe_load(f)
        number_of_stores = Num_of_stores
        store_number = number_of_stores['number_stores']
        store_data = []
        # Iterating through store numbers to download each store data
        for i in range(0, store_number):
            response = requests.get(f"{endpoint}{i}", headers= header)
            data = response.json()
            store_data.append(data)
            
        store_data_df = pd.DataFrame(store_data)
        return store_data_df
    
    def extract_from_s3(self, s3address : str, file_download_path: str = ""):
        '''
        Thus function is used for downloading data from AWS S3 bucket. 
        Using boto3 to connect to AWS S3 client, and downloading data from S3 address.
        Add path of location to download data (default = current working directory). 

        Args:
            S3address (str): Url path string representation, S3 bucket and target file for downloading.
            file_download_path (str): String representation of local path to download target file to.

        Returns:
            df (pd.DataFrame): returns the read target file as a pandas data frame. 
        '''
        s3 = boto3.client('s3')
        # Splitting S3 address into parameters for file downloading
        s3_params = re.split('[//.]', s3address)
        # S3 bucket name from url
        bucket = s3_params[2] 
        # File name by accessing last two elements of split string list
        delimiter = '.'
        target_file = delimiter.join(s3_params[-2:])
        file_download_path = os.getcwd() + '\Data'
        s3.download_file(f'{bucket}',  f'{target_file}', f'{file_download_path}\{target_file}')
        
        def read_in_file(target_file):
            '''
            This function determines the file method for reading in target file. Either .csv or .json file.
            '''
            if '.csv' in target_file:
                s3_df = pd.read_csv(f'{target_file}')
            if '.json' in target_file:
                s3_df = pd.read_json(f'{target_file}')
            return s3_df
        
        res_df = read_in_file(f'{file_download_path}\{target_file}')
        return res_df