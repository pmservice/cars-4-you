# How to setup the Watson Studio project
The sample application requires machine learning models trained and deployed using Watson Studio. 
Please find step by step instruction below.

## Training data set
- upload the [training data set](https://raw.githubusercontent.com/pmservice/wml-sample-models/master/spark/cars-4-you/data/car_rental_training_data.csv) to DB2 Warehouse on Cloud
- in the Watson Studio create a connection to the table 

## Feedback data set and learning system
- upload the [feedback data set](https://raw.githubusercontent.com/pmservice/wml-sample-models/master/spark/cars-4-you/data/car_rental_feedback_data.csv) to DB2 Warehouse on Cloud
- in the Watson Studio create a connection to the table 

## Notebook to train a model, deploy and configure payload logging
- upload a [notebook](https://raw.githubusercontent.com/pmservice/wml-sample-models/master/spark/cars-4-you/notebook/Use%20pySpark%20to%20predict%20Business%20Area%20and%20Action.ipynb) to Watson Studio project
- use `insert to code as spark df` feature to insert the training data table connection (cell [2])
- replace the postgress sql database connection in payload logging section of the notebook (cell [87])
- replace wml_credentials
- run the notebook 

## Configure the learning system
- in the Evaluation section of the model configure learning system by providing connection to feedback table
- set the retrain option to always, redeploy if better
- run new iteration

## Payload logging table and lineage
- in the studio add new connection to the payload logging table to see all scoring results logged
- the lineage can be seen on the lineage tab of the model details


