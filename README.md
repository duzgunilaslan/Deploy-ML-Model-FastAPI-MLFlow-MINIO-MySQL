# Deploy-ML-Model-FastAPI-MLFlow-MINIO-MySQL
This repository about how to deploy machine learning model end serving with FastAPI and using MLFlow-MINIO


![Schema](https://github.com/duzgunilaslan/Deploy-ML-Model-FastAPI-MLFlow-MINIO-MySQL/assets/74202972/af2aeae1-a49d-4e8e-8f1d-d5d4accc5e6a)


# Create a new enviroment
-conda create -n myenv python=3.8

-conda activate myenv

-pip install -r requirements.txt


# Docker run
-docker-compose up -d mysql mlflow minio


# Connect mysql container 

# Connect mysql container 
-docker exec -it mlflow_db mysql -u root -p

# Create database 
-mysql> create database traindatabase;


# Create user 
-mysql> CREATE USER 'trainUser'@'%' IDENTIFIED BY 'Password';


# Grand mlops_user on mlops database 
-mysql> GRANT ALL PRIVILEGES ON traindatabase.* TO 'trainUser'@'%' WITH GRANT OPTION;


-mysql> FLUSH PRIVILEGES;


-mysql> exit



# Train model and register MLFlow
-cd trainModel/
-python trainModelwithMlflow.py

# Run FastAPI
-cd ..
-uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Run Localhost
http://localhost:8002/docs


# Detail Blog



