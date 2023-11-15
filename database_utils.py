class DatabaseConnector:
      '''
      This class will be used to connect to databases. 

      Attributes:
      '''
      # you will use to connect with and upload data to the database
      def __init__(self, db_creds):

            # attributes
            self.db_creds = db_creds

      # methods for connecting to AWS RDS database
      # TODO - read in the db_creds.yaml file
      def read_db_creds(self):
            '''
            Read in the AWS RDS database credentials file. 
            '''
            import yaml
            with open('db_creds.yaml', 'r') as f:
                  self.db_creds = yaml.safe_load(f)
          
      def init_db_engine(self):
            '''
            Read the credentials and initialise to return an sqlalchemy database engine
            '''
            from sqlalchemy import create_engine
            engine = create_engine(connect_args= db_creds)
            engine.execution_options(isolation_level='AUTOCOMMIT').connect()
      
      def list_db_tables(self):
            '''
            To list all tables in database
            '''
            from sqlalchemy import inspect
            inspector = inspect(engine)
            inspector.get_table_names()
      
