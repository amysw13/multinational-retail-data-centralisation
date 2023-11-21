import pandas as pd
import numpy as np
import re

class DataCleaning:

    def check_invalid_input(self, df):
        pattern = re.compile(r"[A-Za-z]+")
        for column in df:
            df[column].astype(str).str.len() == 10 & pattern.match(df[column])

        Index_labels = df[column].index.tolist()
        print(len(Index_labels))
        print(Index_labels)
        df = df.drop(Index_labels, errors='ignore')

    def clean_user_data(self, rds_df):
        '''
        Clean user data, look out for NULL values, errors with dates,
        incorrectly typed values and rows filled with wrong information.

        Create a method called clean_user_data in the DataCleaning class which will perform the cleaning of the user data.
        You will need clean the user data, look out for NULL values, errors with dates, incorrectly typed values and 
        rows filled with the wrong information.
        '''
        rds_df['country_code'] = rds_df['country_code'].replace("GGB", "GB")
        rds_df.date_of_birth = pd.to_datetime(rds_df.date_of_birth,  format= 'mixed', errors='coerce')
        rds_df.join_date = pd.to_datetime(rds_df.join_date,  format= 'mixed', errors='coerce')
        rds_df['address'] = rds_df['address'].str.replace('\n', ' ')
        rds_df = rds_df.dropna()
        isd_code_map = { "GB": "+44", "DE": "+49", "US": "+1" }
        def correct_phone_number(row):
            import re
            # Remove special chars other than digits, `+` and letters used for extension e.g. `x`, `ext` (following keeps all alphabets).
            result = re.sub("[^A-Za-z\d\+]", "", row["phone_number"])
            
            # Prefix ISD code by matching country code.
            if not result.startswith(isd_code_map[row["country_code"]]):
                result = isd_code_map[row["country_code"]] + result

            # Remove `0` that follows ISD code.
            if result.startswith(isd_code_map[row["country_code"]] + "0"):
                result = result.replace(isd_code_map[row["country_code"]] + "0", isd_code_map[row["country_code"]])
            return result

        rds_df["phone_number"] = rds_df.apply(correct_phone_number, axis=1)
        return rds_df  

    def clean_card_data(self, card_df):
        '''
        Cleaning card details dataframe extracted from pdf
        clean the data to remove any erroneous values, 
        NULL values or errors with formatting
        '''
        card_df = pd.concat(card_df) #join list of df into a pandas dataframe
        Index_labels = card_df[card_df['expiry_date'].astype(str).str.len() > 5].index.tolist() #checking invalid values
        card_df = card_df.drop(Index_labels, errors='ignore')
        card_df['card_number'] = card_df['card_number'].replace(r'\D+', np.NaN, regex=True) #retaining only numeric
        card_df.date_payment_confirmed = pd.to_datetime(card_df.date_payment_confirmed, format="%Y-%m-%d", errors="coerce")
        card_df.expiry_date = pd.to_datetime(card_df.expiry_date, format="%m/%y", errors="coerce").dt.strftime("%m/%y")
        card_df = card_df.dropna(how='any')
        card_df['card_number'] = card_df['card_number'].astype('int64')      
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
    
    def clean_events_data(self, events_df):
        #to find wrongly entered information using col 'month' as indicator column
        Index_labels = events_df[events_df['month'].astype(str).str.len() > 2].index.tolist()
        print(len(Index_labels))
        print(Index_labels)
        events_df = events_df.drop(Index_labels, errors='ignore')
        return events_df

