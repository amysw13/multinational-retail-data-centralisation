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
        #TODO - formatting of phone numbers still to work out. 
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
        card_df = pd.concat(card_df) #list of df to pd.df
        card_df = card_df.replace('NULL', np.NaN)
        card_df = card_df.replace('', np.NaN)
        card_df = card_df.dropna()
        card_df['card_number'] = card_df['card_number'].replace(r'\D+', '', regex=True) #retaining only numeric
        card_df = card_df.replace('', np.NaN)
        card_df = card_df.dropna()
        card_df['card_number'] = card_df['card_number'].astype('int64')
        card_df.date_payment_confirmed = pd.to_datetime(card_df.date_payment_confirmed, format="%Y-%m-%d", errors="coerce")
        card_df = card_df.dropna()
        card_df.expiry_date = pd.to_datetime(card_df.expiry_date, format="%m/%y").dt.strftime("%m/%y")
        return card_df

    def called_clean_store_data(self, stores_df):
        '''
        Clean up API retrieved data of store details, and return clean pd.df.
        '''
        stores_df = stores_df.drop('lat', axis=1) #remember to add axis = 1 for dropping column
        stores_df['continent'] = stores_df['continent'].replace("eeEurope", "Europe")
        stores_df['address'] = stores_df['address'].str.replace('\n', ' ')
        stores_df['address'] = stores_df['address'].str.replace(',', ' ')
        stores_df['staff_numbers'] = pd.to_numeric(stores_df['staff_numbers'], errors='coerce')
        stores_df['longitude'] = pd.to_numeric(stores_df['longitude'], errors='coerce')
        stores_df['latitude'] = pd.to_numeric(stores_df['latitude'], errors='coerce')
        stores_df['opening_date'] = pd.to_datetime(stores_df['opening_date'],  format= 'mixed', errors='coerce')
        stores_df = stores_df.replace('NULL', np.NaN)
        stores_df = stores_df.dropna()
        stores_df['staff_numbers'] = stores_df['staff_numbers'].astype('int')
        return stores_df

    def convert_product_weights(self, product_df):
        '''
        If you check the weight column in the DataFrame the weights all have different units.
        Convert them all to a decimal value representing their weight in kg. Use a 1:1 ratio of ml to g as a rough estimate for the rows containing ml.
        Develop the method to clean up the weight column and remove all excess characters then represent the weights as a float.
        '''
        product_df['weight'] = product_df['weight'].str.replace('ml', 'g')
        product_df['weight'] = product_df['weight'].str.replace(' .', '')
        product_df['weight'] = product_df['weight'].dropna()
        #function to evaluate the cells with multiples of weight to total in kg
        def convert_weight(weight):
            if isinstance(weight, str):
                if 'x' in weight:
                    weight = weight.replace('x', '*')
                if 'g' in weight and 'kg' not in weight:
                    weight = eval(weight.replace('g', '')) / 1000  # converting g to kg
                return weight
        product_df['weight'] = product_df['weight'].apply(convert_weight)
        #below, ensure due to mix data types in columns, that only str with kg are replaced, otherwise causes nan in non-str
        product_df['weight'] = product_df['weight'].apply(lambda x: x.replace('kg', '') if isinstance(x, str) else x)
        #finally causes na for unwanted values - will be cleaned up with the next method.
        product_df['weight'] = pd.to_numeric(product_df['weight'], errors='coerce')
        product_df['weight'] = product_df['weight'].round(2)
        return product_df

    def clean_products_data(self, product_df):
        product_df.date_added = pd.to_datetime(product_df.date_added,  format= 'mixed', errors='coerce')
        product_df = product_df.dropna()
        return product_df
    
    def clean_orders_data(self, orders_df):
        orders_df = orders_df.drop(['first_name', 'last_name','1' ,'level_0'], axis=1)
        return orders_df

