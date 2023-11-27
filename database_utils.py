import yaml

from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert


class DatabaseConnector:
      '''
      This class will be used to connect to databases. 

      Attributes:
      db_creds - credentials for connecting to AWS RDS database. 
      '''

      def read_db_creds(self):
            '''
            Read in the AWS RDS database credentials file. 
            '''
            with open('db_creds.yaml', 'r') as f:
                  db_creds = yaml.safe_load(f)
            return db_creds
          
      def init_db_engine(self):
            '''
            Read the credentials from yaml file and adding drivername for sqlalchemy engine connector,
            and initialise to return an sqlalchemy database engine.
            '''
            creds = self.read_db_creds()
            db_url = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
            engine = create_engine(db_url)
            engine.connect()
            return engine
      
      def list_db_tables(self):
            '''
            To list all tables in AWS RDS database
            '''
            inspector = inspect(self.init_db_engine())
            print(inspector.get_table_names())

      def upload_to_db(self, clean_df, table_name):
            '''
            Uploads cleaned dataframes to sales_data database on local machine.
            Cleaned df and given table name as an argument. 
            '''
            with open('local_creds.yaml', 'r') as f:
                  local_creds = yaml.safe_load(f)
            local_db_engine = create_engine(f"{local_creds['DATABASE_TYPE']}+{local_creds['DBAPI']}://{local_creds['USER']}:{local_creds['PASSWORD']}@{local_creds['HOST']}:{local_creds['PORT']}/{local_creds['DATABASE']}")
            local_db_engine.execution_options(isolation_level='AUTOCOMMIT').connect()
            clean_df.to_sql(f'{table_name}', local_db_engine, if_exists='replace')

#Note - this is how the instances will be called.
#Call instances when script is being run automatically,
#and not interactively. 

#connector = database_utils.DatabaseConnector()
#creds = connector.read_db_creds()
#engine = connector.init_db_engine()
#db_list = connector.list_db_tables()