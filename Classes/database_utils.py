import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
import pandas as pd

class DatabaseConnector:
      '''
      DatabaseConnector - a class for connecting to AWS RDS database and centralised database.
      =======================================================================

      DatabaseConnector, contains methods for reading in database credential (yaml) files,
      initiating and engine connector and, list of table names in AWS RDS database.
      A full method, for reading, connecting and uploading a cleaned pandas dataframe to 
      a local machine centralised database. 
      '''

      def read_db_creds(self, filename : str):
            '''
            This function is used to read in the AWS RDS or local database credentials yaml file,
            located in the 'Credentials' directory.

            Args: 
                 

            Returns:
                  variable: returns a named variable with the dictionary of AWS RDS or local database credentials.
            '''
            with open(f'Credentials/{filename}.yaml', 'r') as f:
                  db_creds = yaml.safe_load(f)
            return db_creds
          
      def init_db_engine(self, creds : dict):
            '''
            This function is used to read in the AWS RDS or local database credentials, create a string url for the
            sqlalchemy engine connector and initialise to return an sqlalchemy database engine.

            Args:
                  creds(dict): variable object containing dictionary of database credentials

            Returns:
                  engine(): returns a connected sqlalchemy engine.
            '''
            db_url = f"postgresql://{creds['USER']}:{creds['PASSWORD']}@{creds['HOST']}:{creds['PORT']}/{creds['DATABASE']}"
            engine = create_engine(db_url)
            engine.connect()
            return engine
      
      def list_db_tables(self, engine : Engine):
            '''
            This function is used for listing table names available in the connected
            AWS RDS or local database.

            Args:
                  engine (Engine): name of the engine created to connect to the AWS RDS or local database.

            Returns:
                  Printed list of table names in database.
            '''
            inspector = inspect(engine)
            print(inspector.get_table_names())

      def upload_to_db(self, clean_df : pd.DataFrame , table_name : str, engine : Engine):
            '''
            This function is used to upload a cleaned dataframe into a centralised
            database as a named table. Database connection, to local machine. Reads in local
            database credentials in 'local_creds.yaml' file located in the 'Credentials' directory.

            Args:
                  clean_df (pd.DataFrame): variable object of cleaned pandas dataframe
                  table_name (str): string representation of table name for cleaned 
                  dataframe to be named in centralised database.
                  engine (Engine): name of the engine created to connect to the AWS RDS or local database.
            '''
                  
            engine.execution_options(isolation_level='AUTOCOMMIT').connect()
            clean_df.to_sql(f'{table_name}', engine, if_exists='replace')