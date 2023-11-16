import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect


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

      def upload_to_db(self):
            '''
            Take user_df and table name to upload as an argument. 
            '''
            self.user_df.to_sql('dim_users', self.engine, if_exists='replace')

#Note - this is how the instances will be called.
#Call instances when script is being run automatically,
#and not interactively. 

#connector = DatabaseConnector()
#creds = connector.read_db_creds()
#engine = connector.init_db_engine()
#db_list = connector.list_db_tables()