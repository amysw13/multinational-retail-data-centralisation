import pandas as pd
import numpy as np

class DataCleaning:

    def clean_user_data(self, rds_df):
        '''
        Clean user data, look out for NULL values, errors with dates,
        incorrectly typed values and rows filled with wrong information.

        Create a method called clean_user_data in the DataCleaning class which will perform the cleaning of the user data.
        You will need clean the user data, look out for NULL values, errors with dates, incorrectly typed values and 
        rows filled with the wrong information.
        '''
        #No null data to begin with
        #2. Address - need to remove and replace "\n" - formatting
        #3. Check date formats - currently object (str/mixed data) -> change to datetime64
        #4. remove all null values .dropna()
        #TODO - run through the columns for data type conversion to dates, 
        # formatting of addresses, and clean up all null values. 

        rds_df.date_of_birth = pd.to_datetime(rds_df.date_of_birth,  format= 'mixed', errors='coerce')
        rds_df.join_date = pd.to_datetime(rds_df.join_date,  format= 'mixed', errors='coerce')
        rds_df['address'] = rds_df['address'].str.replace('\n', ' ')
        rds_df = rds_df.dropna()   
        return rds_df  

    def clean_card_data(self, card_df):
        '''
        Cleaning card details dataframe extracted from pdf
        clean the data to remove any erroneous values, 
        NULL values or errors with formatting
        '''
        #TODO - review cols for numeric and formatting clean up
        card_df = pd.concat(card_df) #list of df to pd.df
        card_df = card_df.replace('NULL', np.NaN)
        card_df = card_df.replace('', np.NaN)
        card_df = card_df.dropna()
        card_df['card_number'] = card_df['card_number'].replace(r'\D+', '', regex=True)
        card_df = card_df.replace('', np.NaN)
        card_df = card_df.dropna()
        card_df['card_number'] = card_df['card_number'].astype('int64')
        card_df.date_payment_confirmed = pd.to_datetime(card_df.date_payment_confirmed, format="%Y-%m-%d", errors="coerce")
        card_df = card_df.dropna()
        card_df.expiry_date = pd.to_datetime(card_df.expiry_date, format="%m/%y").dt.strftime("%m/%y")
        return card_df

    def called_clean_store_data(self, stores_df):
        '''
        Clean up API retrieved data of store details.
        '''
        #TODO:
        # - delete/drop lat column
        # - continent - Spelling/formatting 'eeEurope'
        # - opening_data - formatting to datetime
        # - address - formatting
        # - longitude - consistent formatting
        # - remove rows of wrong/ NULL data /
        stores_df = stores_df.replace('NULL', np.NaN)

