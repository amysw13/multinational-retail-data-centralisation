import pandas as pd
import tabula
import os

os.environ["JAVA_HOME"] = "C:/Program Files/Java/jdk-21"

class DataExtractor:
    ''' 
    This class is for extracting data from different data sources

    This class will include methods for extracting data from .csv, APIs and AWS RDS.
    contain methods to help extract data from different data sources - CSV files - API - S3 bucket.
    Attributes:
    (Do I need to set certain permissions, private etc...?)
    '''
    def read_rds_table(self, table, engine):
        '''
        Using list_db_tables from DatabaseConnector Class - read in table of user data. 
        '''
        user_df = pd.read_sql_table(f"{table}", engine)
        return user_df
    
    def retrieve_pdf_data():
        pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        card_details_df = tabula.read_pdf(pdf_path, pages= 'all')
        return card_details_df

#extractor = DataExtractor()