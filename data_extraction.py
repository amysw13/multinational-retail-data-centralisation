import os

import tabula
import requests
import boto3
import re

import pandas as pd

os.environ["JAVA_HOME"] = "C:/Program Files/Java/jdk-21"

class DataExtractor:
    ''' 
    This class is for extracting data from different data sources

    This class will include methods for extracting data from .pdf, .csv and .json files, APIs, s3 buckets and AWS RDS.
    Returning the data as pandas data frames for cleaning and uploading to centralised data base. 
    '''
    def read_rds_table(self, table, engine):
        '''
        Using list_db_tables from DatabaseConnector Class - read in table of user data. 
        '''
        user_df = pd.read_sql_table(f"{table}", engine)
        return user_df
    
    def retrieve_pdf_data(self):
        pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        card_details_df = tabula.read_pdf(pdf_path, pages= 'all')
        return card_details_df
    
    def list_number_of_stores(self, endpoint, header):
        #endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
        #header = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        response = requests.get(f"{endpoint}", headers=header)
        Num_of_stores = response.json()
        return Num_of_stores

    def retrieve_stores_data(self, Num_of_stores, endpoint):
        #NOTE -  this is a time bottleneck
        #Note - remove {store_number} for final endpoint url
        #endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
        header = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        number_of_stores = Num_of_stores
        store_number = number_of_stores['number_stores']
        store_data = []
        for i in range(1, store_number):
            response = requests.get(f"{endpoint}{i}", headers= header)
            data = response.json()
            store_data.append(data)
        
        store_data_df = pd.DataFrame(store_data)
        return store_data_df
    
    def extract_from_s3(self, s3address):
        s3 = boto3.client('s3')
        #s3address = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
        #s3address = 's3://data-handling-public/products.csv'
        s3_params = re.split('[//.]', s3address)
        #bucket name from url
        bucket = s3_params[2] 
        #file name by accessing last two elements of split string list
        delimiter = '.'
        target_file = delimiter.join(s3_params[-2:])
        file_download_path = 'C:/Users/amysw/Documents/AI_core/multinational-retail-data-centralisation/'
        s3.download_file(f'{bucket}',  f'{target_file}', f'{file_download_path}{target_file}')
        def read_in_file(target_file):
            if '.csv' in target_file:
                s3_df = pd.read_csv(f'{target_file}')
            if '.json' in target_file:
                s3_df = pd.read_json(f'{target_file}')
            return s3_df
        res_df = read_in_file(target_file)
        return res_df