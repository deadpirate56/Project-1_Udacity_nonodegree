# Disaster Response Project

## Summary

In the Project, we'll find a data set containing real messages that were sent during disaster events. We will be creating a machine learning pipeline to categorize these events so that one can categorize and send the messages to an appropriate disaster relief agency.


## Project Components
There are three components to this project.

## 1. ETL Pipeline
In a Python script, process_data.py, write a data cleaning pipeline that:
1. Loads the messages and categories datasets
2. Merges the two datasets
3. Cleans the data
4. Stores it in a SQLite database
## 2. ML Pipeline
In a Python script, train_classifier.py, write a machine learning pipeline that:
1. Loads data from the SQLite database
2. Splits the dataset into training and test sets
3. Builds a text processing and machine learning pipeline
4. Trains and tunes a model using GridSearchCV
5. Outputs results on the test set
6. Exports the final model as a pickle file
## 3. Flask Web App
We are providing much of the flask web app for you, but feel free to add extra features depending on your knowledge of flask, html, css and javascript. For this part, you'll need to:

1. Modify file paths for database and model as needed
2. Add data visualizations using Plotly in the web app. One example is provided for you
# Disaster Response Pipeline Project

### Files in the Repository section
app
| - template
| |- master.html # main page of web app
| |- go.html # classification result page of web app
|- run.py # Flask file that runs app
data
|- disaster_categories.csv # data to process
|- disaster_messages.csv # data to process
|- process_data.py

models
|- train_classifier.py

ETL Pipeline ipynb file # file on which the process_data.py file is based on
ML P[ipeline ipynb filr # File on which train_classifier.py file is based on


README.md



### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Go to `app` directory: `cd app`

3. Run your web app: `python run.py`

4. Click the `PREVIEW` button to open the homepage
