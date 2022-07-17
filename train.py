import pandas as pd

from helper.data_check_preparation import read_and_check_data
from helper.pipeline_cleansing import pipeline_cleansing


def train_model():
    # pembacaan dan pengecekan data
    df = read_and_check_data(PATH)
    
    # feature engineering
    df_transformed = pipeline_cleansing(df)
    print("Start Saving Result Cleansing Data!")
    df_transformed.to_csv("artifacts/df_transformed.csv")
    