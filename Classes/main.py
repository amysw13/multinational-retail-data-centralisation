import database_utils as db_utils
import data_extraction as data_ext
import data_cleaning as data_clean

if __name__ == '__main__':
    # Create instances of each class
    connector = db_utils.DatabaseConnector()
    extractor = data_ext.DataExtractor()
    cleaning = data_clean.DataCleaning()

    # Reading in AWS RDS database credentials from .yaml file.
    creds = connector.read_db_creds()
    # Create engine and connecting to AWS RDS database.
    engine = connector.init_db_engine()
    # Printing list of available tables names in AWS RDS database
    db_list = connector.list_db_tables()

    # User data
    # Download data from 'legacy_users' table, using the AWS RDS specified connection engine.
    rds_df = extractor.read_rds_table('legacy_users', engine)
    # Cleaning user data
    clean_rds_df = cleaning.clean_user_data(rds_df)
    # Uploading dataframe to centralised database
    connector.upload_to_db(clean_rds_df, 'dim_users')
    print('User data complete and uploaded')

    # Card data
    # Extracting data
    card_df = extractor.retrieve_pdf_data()
    # Cleaning card details data
    clean_card_df = cleaning.clean_card_data(card_df)
    # Upload cleaned data to local database
    connector.upload_to_db(clean_card_df, 'dim_card_details')
    print('Card data complete and uploaded')

    # Store details data
    num_stores = extractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',{'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'} )
    stores_df = extractor.retrieve_stores_data(num_stores,'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/')
    clean_stores_df = cleaning.clean_store_data(stores_df)
    connector.upload_to_db(clean_stores_df, 'dim_store_details')
    print('Store details data complete and uploaded')

    # Product details data
    product_df = extractor.extract_from_s3('s3://data-handling-public/products.csv')
    product_df_weight = cleaning.convert_product_weights(product_df)
    clean_product_df = cleaning.clean_products_data(product_df_weight)
    connector.upload_to_db(clean_product_df, 'dim_products')
    print('Product details data complete and uploaded')

    # Order data
    orders_df = extractor.read_rds_table('orders_table', engine)
    clean_orders_df = cleaning.clean_orders_data(orders_df)
    connector.upload_to_db(clean_orders_df, 'orders_table')
    print('Order data complete and uploaded')

    # Events data
    events_df = extractor.extract_from_s3('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json')
    clean_event_df = cleaning.clean_events_data(events_df)
    connector.upload_to_db(clean_event_df, 'dim_date_times')
    print('Events data complete and uploaded')
    print('All Done!')