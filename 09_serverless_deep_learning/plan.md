# 9. Serverless Deep Learning

We'll deploy the clothes classification model we trained previously. 

## 9.1 Introduction to Serverless 

* What we'll cover this week


## 9.2 AWS Lambda

* Intro to AWS Lambda
* Serverless vs serverfull


## 9.3 TensorFlow Lite

* Why not TensorFlow
* Converting the model
* Using the TF-Lite model for making predictions


## 9.4 Preparing the Lambda code

* Moving the code from notebook to script
* Testing it locally


## 9.5 Preparing a Docker image

* Lambda base images
* Preparing the Dockerfile
* Using the right TF-Lite wheel

docker build -t clothing-model .  
docker run -it --rm -p 8080:8080 clothing-model:latest


## 9.6 Creating the lambda function

* Publishing the image to AWS ECR
* Creating the function
* Configuring it
* Testing the function from the AWS Console
* Pricing

pip install awscli (version 2)  

aws sso login --profile <profile_name>

aws ecr create-repository --repository-name clothing-tflite-images --profile <profile_name>  

aws ecr get-login-password --region eu-west-3 --profile <profile_name> | docker login --username AWS --password-stdin 886436962520.dkr.ecr.eu-west-3.amazonaws.com

REGISTRY=clothing-tflite-images  
TAG=clothing-model-xception-v4-001  
PREFIX=${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY}  
REMOTE_URI=${PREFIX}:${TAG}  

docker tag clothing-model:latest ${REMOTE_URI}  
docker push ${REMOTE_URI}



## 9.7 API Gateway: exposing the lambda function

* Creating and configuring the gateway


## 9.8 Summary 

* AWS Lambda is way of deploying models without having to worry about servers
* Tensorflow Lite is a lightweight alternative to Tensorflow that only focuses on inference
* To deploy your code, package it in a Docker container
* Expose the lambda function via API Gateway


## 9.9 Explore more

* Try similar serverless services from Google Cloud and Microsoft Azure
* Deploy cats vs dogs and other Keras models with AWS Lambda
* AWS Lambda is also good for other libraries, not just Tensorflow. You can deploy Scikit-Learn and XGBoost models with it as well.