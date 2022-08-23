import sys

import numpy as np 
import pandas as pd 

# Data Visualization
import seaborn as sns
import matplotlib.pyplot as plt 
import json

#importing sqlite
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    Loads and merges datasets from 2 filepaths.
    
    Parameters:
    messages_filepath: messages csv file
    categories_filepath: categories csv file
    
    Returns:
    df: dataframe containing messages_filepath and categories_filepath merged
    
    """
    # loading datasets
    messages = pd.read_csv(messages_filepath)
    categories =  pd.read_csv(categories_filepath)
    #merging datasets
    df = messages.merge(categories,how ='outer',left_on = 'id', right_on = 'id')
    return df


def clean_data(df):
    
    """
    Cleans the dataframe
    
    Parameters:
    df: DataFrame
    
    Returns:
    df: Cleaned DataFrame
    
    """
    #expanding category columns-
    categories = df['categories'].str.split(';', expand=True)
    
    # select the first row of the categories dataframe
    row = categories.head(1)
    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything 
    # up to the second to last character of each string with slicing
    category_colnames =  row.applymap(lambda x: x[:-2]).iloc[0,:]
    # rename the columns of `categories`
    categories.columns = category_colnames
    for column in categories:
        categories[column] = categories[column].apply(lambda x : x[-1:])
        categories[column] = categories[column].astype(int)
        
    # drop the original categories column from `df`
    df.drop('categories', axis = 1, inplace = True)
    df = df.merge(categories, left_index = True, right_index = True)
    
    # drop duplicates
    df.drop_duplicates(inplace = True)
    
    #replacing null values by 0 in categories columns
    for column in categories.columns:
        df[column] = df[column].fillna(0)
    
    # return clean data
    return df


def save_data(df, database_filename):
    """Stores df in a SQLite database
    
    Parameters : df
    
    """
    # storing the final file in sql database
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('classified_messages', engine, index=False, if_exists='replace') 
    


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
