import sys
# import libraries
import pandas as pd
import numpy as np
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import os
import urllib.request
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_multilabel_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import  TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import recall_score
import sklearn
import pickle


nltk.download(['punkt', 'wordnet','stopwords'])

def load_data(database_filepath):
    # load data from database
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table("classified_messages", con=engine)
    # Defining Target and Feature tables
    X = df['message']
    Y = df.iloc[: , 4:]
    return X, Y


def tokenize(text):
    
    tokens = word_tokenize (text)
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    final_tokens = [lemmatizer.lemmatize(x).lower().strip() for x in tokens if not x.lower() in stop_words]
    
    return final_tokens
    


def build_model():
    
    #Building model
    clf = RandomForestClassifier()
    
    #building the pipeline
    pipeline = Pipeline ([ ('count', CountVectorizer(tokenizer=tokenize)),
                        ('vect', TfidfTransformer()),
                      ('clf', MultiOutputClassifier(clf))])
    
    
    
    parameters = {'clf__estimator__max_depth': [5,8],'clf__estimator__n_estimators' :  [100,400]}
    grid_cv =  GridSearchCV(pipeline, param_grid= parameters)
                
    return grid_cv


def evaluate_model(model, X_test, Y_test):
    Y_pred = model.predict(X_test)
    for index, column in enumerate(Y_test):
        print(column, classification_report(Y_test[column], Y_pred[:, index]))


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()