## 10.1 Overview

We'll deploy the clothes classification model we trained 
previously using Kubernetes and TensorFlow Serving

* What we'll cover this week
* Two-tier architecture
* 1st component: gateway (download image, resize, turn into numpy array - computationally not expensive - can be done with CPU)
* 2nd component: model (matrix multiplications - computationally expensive - thus use GPU)
* scaling the two components independently: i.e. 5 gateways handing images to 1 model

## 10.2 TensorFlow Serving

using tensorflow serving, written in C++, with focus on inference

* The saved_model format
* Running TF-Serving locally with Docker
* Invoking the model from Jupyter
* gRPC binary protocol

## 10.3 Creating the pre-processing Flask service

* Converting the notebook to a Python script
* Wrapping the script into a Flask app
* Creating the virtual env with Pipenv
* Getting rid of the tensorflow dependency

## 10.4 Running everything locally with Docker-compose

two components in two different docker container

* Preparing the images 
* Installing docker-compose 
* Running the service 
* Testing the service

## 10.5 Introduction to Kubernetes

* kubernetes main concepts
* The anatomy of a Kubernetes cluster

## 10.6 Deploying a simple service to Kubernetes

running kubernetes on your local machine

* Create a simple ping application in Flask
* Installing kubectl
* Setting up a local Kubernetes cluster with Kind
* Creating a deployment
* Creating a service 

## 10.7 Deploying TensorFlow models to Kubernetes

* Deploying the TF-Serving model
* Deploying the Gateway
* Testing the service

## 10.8 Deploying to EKS

move from local to cloud

* Creating a EKS cluster on AWS
* Publishing the image to ECR

## 10.9 Summary

* TF-Serving is a system for deploying TensorFlow models
* When using TF-Serving, we need a component for pre-processing 
* Kubernetes is a container orchestration platform
* To deploy something on Kubernetes, we need to specify a deployment and a service
* You can use Docker compose and Kind for local experiments 

## 10.10 Explore more

* Other local Kuberneteses: minikube, k3d, k3s, microk8s, EKS Anywhere
* [Rancher desktop](https://rancherdesktop.io/)
* Docker desktop
* [Lens](https://k8slens.dev/)
* Many cloud providers have Kubernetes: GCP, Azure, Digital ocean and others. Look for "Managed Kubernetes" in your favourite search engine
* Deploy the model from previous modules and from your project with Kubernetes
* Learn about Kubernetes namespaces. Here we used the default namespace