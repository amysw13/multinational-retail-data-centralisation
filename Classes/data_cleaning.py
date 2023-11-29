import pandas as pd
import numpy as np
import re

class DataCleaning:
    '''
    DataCleaning - a class for cleaning raw data extracted from the DataExtractor class.
    =======================================================================

    DataCleaning, contains methods for cleaning specific data frames extracted from 
    multiple data sources. Cleaning includes, removing and converting NULL values,
    date errors and datetime transformation, correcting and formatting incorrectly typed
    values and, removing rows of wrongly filled information.
    '''
    def clean_user_data(self, user_df):
        '''
        This function is used for cleaning user data by correcting incorrectly input information,
        cleaning up formatting in address, and converting 'date_of_birth' and 'join_date' into
        consistent datetime format. With sub-function for cleaning up phone numbers based on
        'country_codes'.

        Args:
            user_df (pd.Dataframe): variable object of AWS RDS downloaded user data.

        Returns
            dataframe (pd.Dataframe): returns cleaned data frame of pd.Dataframe.
        '''
        user_df['country_code'] = user_df['country_code'].replace("GGB", "GB")
        user_df['date_of_birth'] = pd.to_datetime(user_df['date_of_birth'] ,  format= 'mixed', errors='coerce')
        user_df['join_date'] = pd.to_datetime(user_df['join_date'],  format= 'mixed', errors='coerce')
        user_df['address'] = user_df['address'].str.replace('\n | ', ' ')
        user_df = user_df.dropna()

        isd_code_map = { "GB": "+44", "DE": "+49", "US": "+1" }
        def correct_phone_number(row):
            '''
            This function is used to clean up phone numbers based on country codes. 
            By Remove special chars other than digits, `+` and letters used for extension e.g. `x`, `ext`, 
            matching country code and inputting country pre-fix if not present and 
            removing "0" and adding in "+" for consistent phone number format.
            '''
            result = re.sub("[^A-Za-z\d\+]", "", row["phone_number"])
            
            if not result.startswith(isd_code_map[row["country_code"]]):
                result = isd_code_map[row["country_code"]] + result

            if result.startswith(isd_code_map[row["country_code"]] + "0"):
                result = result.replace(isd_code_map[row["country_code"]] + "0", isd_code_map[row["country_code"]])
            return result

        user_df["phone_number"] = user_df.apply(correct_phone_number, axis=1)
        return user_df  

    def clean_card_data(self, card_df):
        '''
        This function is used for cleaning card details dataframe extracted from pdf. 
        Removes any erroneous values, formatting errors, transforming 'card_number' to int64 and
        converting 'date_payment_confirmed' in to consistent datetime format.

        Args:
            card_df (pd.Dataframe): variable object of pdf downloaded card details data.

        Returns
            dataframe (pd.Dataframe): returns cleaned data frame of pd.Dataframe.
        '''
        card_df = card_df[card_df['expiry_date'].astype(str).str.len() == 5] #keeping rows on condition expiry date string is length = 5.
        card_df['card_number'] = card_df['card_number'].replace(regex=[r'\D+'], value="")  #retaining only numeric
        card_df['card_number'] = card_df['card_number'].astype('int64')
        card_df['date_payment_confirmed'] = pd.to_datetime(card_df['date_payment_confirmed'], format='mixed', errors="coerce")
        return card_df

    def clean_store_data(self, stores_df):
        '''
        This function is used for cleaning stores data frame retrieved from web APIs. 
        Cleaning removed erroneous values, converting and formatting incorrectly formatted values, formatting and
        transforming dates to consistent datetime format, converting 'N/A' and 'None' strings to NAs, and dropping
        'lat' column, returning a cleaned pandas dataframe.

        Args:
            card_df (pd.Dataframe): variable object of web API downloaded store details data.

        Returns
            dataframe (pd.Dataframe): returns cleaned data frame of pd.Dataframe.
        '''
        stores_df = stores_df[stores_df['country_code'].astype(str).str.len() == 2]
        stores_df['staff_numbers'] = stores_df['staff_numbers'].replace(regex=[r'\D+'], value="").astype('int')  #retaining only numeric
        stores_df['continent'] = stores_df['continent'].replace("eeEurope" , "Europe" )
        stores_df['continent'] = stores_df['continent'].replace("eeAmerica" , "America")
        stores_df['opening_date'] = pd.to_datetime(stores_df['opening_date'],  format= 'mixed', errors='coerce')
        stores_df['address'] = stores_df['address'].replace('\\n|,\s', ' ', regex = True)
        stores_df = stores_df.replace({'N/A': np.nan, None: np.nan})
        stores_df = stores_df.drop('lat', axis=1) #remember to add axis = 1 for dropping column
        return stores_df

    def convert_product_weights(self, product_df):
        '''
        This function is used for converting product weight data to a standardised weight of kilograms.
        Weights in ml converted to grams at a 1:1 ratio. Returns converted values as kg (float) to 2 decimal places.

        Args:
            product_df (pd.Dataframe): variable object of product data frame with a column of weight values named 'weight'.
        Returns:
            df (pd.Dataframe): data frame weight column converted into kg (float) to two decimal places.

        '''
        product_df['weight'] = product_df['weight'].replace(regex=[r'ml'], value='g')
        product_df['weight'] = product_df['weight'].replace(regex=[r'\s\.'], value='')
        product_df['weight'] = product_df['weight'].replace('16oz', 0.45)
        #function to evaluate the cells with multiples of weight to total in kg
        def convert_weight(row):
            '''
            This function takes values in 'weight' column and converts multiples of weights
            and evaluates to total product weight in kg.
            '''
            if isinstance(row['weight'], str):
                if 'x' in row['weight']:
                    row['weight'] = row['weight'].replace('x', '*')
                if 'g' in row['weight'] and 'kg' not in row['weight']:
                    row['weight'] = eval(row['weight'].replace('g', '')) / 1000  # converting g to kg
            return row['weight']
        product_df['weight'] = product_df.apply(convert_weight, axis =1)
        #below, ensure due to mix data types in columns, that only str with kg are replaced, otherwise causes nan in non-str
        product_df['weight'] = product_df['weight'].apply(lambda x: x.replace('kg', '') if isinstance(x, str) else x)
        #finally causes na for unwanted values - will be cleaned up with the next method.
        product_df['weight'] = pd.to_numeric(product_df['weight'], errors='coerce')
        product_df['weight'] = product_df['weight'].round(2)
        return product_df

    def clean_products_data(self, product_df):
        '''
        This function is used for cleaning product data downloaded from AWS s3 bucket. 
        Data is of date_added converted to consistent datetime format and any NA values dropped.
        Returning a cleaned pandas data frame.
        
        Args:
            product_df (pd.Dataframe): variable object of product data downloaded from AWS s3 bucket.
        Returns:
            df (pd.Dataframe): returns cleaned data frame of pd.Dataframe.
        '''
        product_df['date_added'] = pd.to_datetime(product_df['date_added'],  format= 'mixed', errors='coerce')
        product_df = product_df.dropna()
        return product_df
    
    def clean_orders_data(self, orders_df):
        '''
        This function is used for cleaning order data downloaded from AWS RDS database.
        Removing unnecessary columns - 'first_name', 'last_name','1' ,'level_0'.

        Args:
            orders_df (pd.Dataframe): variable object of AWS RDS downloaded orders data.

        Returns
            dataframe (pd.Dataframe): returns cleaned data frame of pd.Dataframe.
        '''
        orders_df = orders_df.drop(['first_name', 'last_name','1' ,'level_0'], axis=1)
        return orders_df
    
    def clean_events_data(self, events_df):
        '''
        This function is used for cleaning events data downloaded from AWS s3 bucket.
        Checks and removes for any incorrectly input values.

        Args:
            events_df (pd.Dataframe): variable object of AWS s3 downloaded events data.

        Returns
            dataframe (pd.Dataframe): returns cleaned data frame of pd.Dataframe.
        '''        
        events_df =  events_df[events_df['month'].astype(str).str.len() == 2]
        return events_df

