import pandas as pd
import numpy as np
from helper.preprocessing import normalize

def pipeline_cleansing(df):
    # Change column name from camelCase to snake_case
    change_to_snakecase = {"dateCreated": "ad_created",
                    "dateCrawled": "date_crawled",
                    "fuelType": "fuel_type",
                    "lastSeen": "last_seen",
                    "monthOfRegistration": "registration_month",
                    "notRepairedDamage": "unrepaired_damage",
                    "nrOfPictures": "num_of_pictures",
                    "offerType": "offer_type",
                    "postalCode": "postal_code",
                    "powerPS": "power_ps",
                    "vehicleType": "vehicle_type",
                    "yearOfRegistration": "registration_year"}
    df.rename(columns= change_to_snakecase, inplace=True)
    
    # convert to datetime
    column_date = ["ad_created", "date_crawled", "last_seen"]
    df[column_date] = df[column_date].apply(pd.to_datetime)

    # convert numerical variable to int 
    df['price'] = df['price'].str.replace('$','').str.replace(',','')
    df['odometer'] = df['odometer'].str.replace('km','').str.replace(',','')
    df[['price','odometer']] = df[['price','odometer']].astype('int64')

    # drop column that many unique value, contains 0, imbalance    
    drop_col_category = ['name','model','brand','postal_code','num_of_pictures']
    df.drop(columns=drop_col_category, inplace=True)

    # handling outlier of target variable
    df = df[(df['price'] >= 500) & (df['price'] <= 40000)]

    # fill null value by mode (categorical)
    df['vehicle_type'].fillna(df['vehicle_type'].mode()[0], inplace=True)
    df['gearbox'].fillna(df['gearbox'].mode()[0], inplace=True)
    df['fuel_type'].fillna(df['fuel_type'].mode()[0], inplace=True)
    df['unrepaired_damage'].fillna(df['unrepaired_damage'].mode()[0], inplace=True)
    
    # normalized for data numeric except price
    data_numeric = df[['registration_year','power_ps','odometer','registration_month']]
    data_normalize = normalize(data_numeric)
        
    # get dummies for data categorical
    data_category = df[['seller','offer_type','abtest','vehicle_type','gearbox','fuel_type','unrepaired_damage']]
    data_category1 = pd.get_dummies(data_category)
    
    # get data price
    data_price = df[['price']]
    
    # join dataframe to one
    data_numerical = data_price.join(data_normalize)
    df_transformed = data_numerical.join(data_category1)

    return df_transformed