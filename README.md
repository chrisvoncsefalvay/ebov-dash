# Dash demo: W African EBOV Outbreak

A Dash application to explore the [UN Humanitarian Data Exchange (HDX)](https://data.humdata.org/) 
data on the [West African Ebola outbreak](https://data.humdata.org/dataset/ebola-cases-2014/resource/c59b5722-ca4b-41ca-a446-472d6d824d01).
Made as a simple app to demonstrate deploying Dash apps using Docker on
AWS's Elastic Container Service (ECS). 

This repo was created to accompany the Medium article on deploying 
dockerised Dash apps on AWS.

## Local development

1. Create a Python venv with a >=3.6 interpreter.

2. Activate venv (`source <venv path>/bin/activate`).

3. Install Python dependencies using `pip3 install -r requirements.txt`.

4. Run the server using `python3 wsgi.py`.


## Running locally

To run a local instance, the easiest way is to build the Docker image:

1. Build the image using `docker build -t ebov-dash .`. 

2. Run the image using `docker run -p 80:8080 ebov-dash:latest`.

3. Use your browser to navigate to `127.0.0.1:8080` to view the application.

## Deploying onto AWS FARGATE

When making changes, you need to rebuild the Docker image and push it to AWS
ECR, then re-deploy.

1. Run `$(aws ecr get-login --no-include-email --region eu-central-1)` 
to authenticate your shell.

2. Build the image using `docker build -t ebov-dash .`.

3. Tag the image using `docker tag ebov-dash:latest <your account id>.dkr.ecr.<your AWS region>.amazonaws.com/ebov-dash:latest`.

4. Push the image to AWS ECR using `docker push <your account id>.dkr.ecr.<your AWS region>.amazonaws.com/ebov-dash:latest`.

5. Create a new FARGATE instance or update the running FARGATE instance 
with the Update button at the EBOV Dash ECS page.

---------

When deploying onto a new server, 1 vCPU and 2GB memory are the absolute
 minimum necessary for decent operation. More is better, as quite a bit
 of data related calculations are run in the background.
