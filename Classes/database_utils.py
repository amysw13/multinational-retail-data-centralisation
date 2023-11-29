import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:
      '''
      DatabaseConnector - a class for connecting to AWS RDS database and centralised database.
      =======================================================================

      DatabaseConnector, contains methods for reading in database credential (yaml) files,
      initiating and engine connector and, list of table names in AWS RDS database.
      A full method, for reading, connecting and uploading a cleaned pandas dataframe to 
      a local machine centralised database. 
      '''

      def read_db_creds(self):
            '''
            This function is used to read in the AWS RDS database credentials yaml file,
            located in the 'Credentials' directory.

            Returns:
                  variable: returns a named variable with the dictionary of AWS RDS database credentials.
            '''
            with open('Credentials/db_creds.yaml', 'r') as f:
                  db_creds = yaml.safe_load(f)
            return db_creds
          
      def init_db_engine(self):
            '''
            This function is used to read in the AWS RDS credentials, create a string url for the
            sqlalchemy engine connector and initialise to return an sqlalchemy database engine.

            Returns:
                  engine(): returns a connected sqlalchemy engine.
            '''
            creds = self.read_db_creds()
            db_url = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
            engine = create_engine(db_url)
            engine.connect()
            return engine
      
      def list_db_tables(self):
            '''
            This function is used for listing table names available in the connected
            AWS RDS database.

            Returns:
                  Printed list of table names in database.
            '''
            inspector = inspect(self.init_db_engine())
            print(inspector.get_table_names())

      def upload_to_db(self, clean_df, table_name):
            '''
            This function is used to upload a cleaned dataframe into a centralised
            database as a named table. Database connection, to local machine. Reads in local
            database credentials in 'local_creds.yaml' file located in the 'Credentials' directory.

            Args:
                  clean_df (pd.Dataframe): variable object of cleaned pandas dataframe
                  table_name (str): string representation of table name for cleaned 
                  dataframe to be named in centralised database.
            '''
            with open('Credentials/local_creds.yaml', 'r') as f:
                  local_creds = yaml.safe_load(f)
            local_db_engine = create_engine(f"{local_creds['DATABASE_TYPE']}+{local_creds['DBAPI']}://{local_creds['USER']}:{local_creds['PASSWORD']}@{local_creds['HOST']}:{local_creds['PORT']}/{local_creds['DATABASE']}")
            local_db_engine.execution_options(isolation_level='AUTOCOMMIT').connect()
            clean_df.to_sql(f'{table_name}', local_db_engine, if_exists='replace')