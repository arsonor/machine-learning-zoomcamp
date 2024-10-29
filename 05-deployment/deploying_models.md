# 5. Deploying Machine Learning models 

We'll use the same model we trained and evaluated
previously - the churn prediction model. Now we'll
deploy it as a web service.

## 5.1 Intro / Session overview

* What we will cover this week

## 5.2 Saving and loading the model

* Saving the model to pickle
* Loading the model from pickle
* Turning our notebook into a Python script

## 5.3 Web services: introduction to Flask

* Writing a simple ping/pong app
* Querying it with `curl` and browser

## 5.4 Serving the churn model with Flask

* Wrapping the predict script into a Flask app
* Querying it with `requests` 
* Preparing for production: gunicorn
* Running it on Windows with waitress

## 5.5 Python virtual environment: Pipenv

* Dependency and environment management
* Why we need virtual environment
* Installing Pipenv
* Installing libraries with Pipenv
* Running things with Pipenv

## 5.6 Environment management: Docker

* Why we need Docker
* Running a Python image with docker
* Dockerfile
* Building a docker image
* Running a docker image

## 5.7 Deployment to the cloud: AWS Elastic Beanstalk (optional)

* Installing the eb cli
* Running eb locally
* Deploying the model

## 5.8 Summary and Application

* **Save models with pickle**

If you don't have the model from the previous chapter, run `05-deploy.ipynb` to generate the pickle file.

* **Use Flask to turn the model into a web service**

First, install flask:

```bash
pip install flask
```

Run the service:

```bash
python churn_serving.py
```

Test it from python:

```python
import requests
url = 'http://localhost:9696/predict'
response = requests.post(url, json=customer)
result = response.json()
```

 - Until here we saw how we made a simple web server that predicts the churn value for every user. When you run your app you will see a warning that it is not a WGSI server and not suitable for production environmnets. To fix this issue and run this as a production server there are plenty of ways available. 
   - One way to create a WSGI server is to use gunicorn. To install it use the command ```pip install gunicorn```, And to run the WGSI server you can simply run it with the   command ```gunicorn --bind 0.0.0.0:9696 churn:app```. Note that in __churn:app__ the name churn is the name we set for the file containing the code ```app = Flask('churn')```(for example: churn.py), You may need to change it to whatever you named your Flask app file.  
   -  Windows users may not be able to use gunicorn library because windows system do not support some dependecies of the library. So to be able to run this on a windows machine, there is an alternative library waitress and to install it, just use the command ```pip install waitress```. 
   -  to run the waitress wgsi server use the command ```waitress-serve --listen=0.0.0.0:9696 churn:app```.
   -  To test it, you can run the code above and the result will be the same.

* **Use a dependency & env manager**

Install `pipenv`:

```bash
pip install pipenv
```

Install the depencencies from the [Pipfile](Pipfile):

```bash
pipenv install
```

Enter the pipenv virtual environment:

```bash
pipenv shell
```

And run the code:

```bash
python churn_serving.py
```

Alternatively, you can do both steps with one command:

```bash
pipenv run python churn_serving.py
```

Now you can use the same code for testing the model locally.

* **Package it in Docker**

Build the image (defined in [Dockerfile](Dockerfile))

```bash
docker build -t churn-prediction .
```

Run it:

```bash
docker run -it -p 9696:9696 churn-prediction:latest
```

* **Deploy to the cloud**

```bash
pipenv install awsebcli --dev
```

```bash
eb init --profile martin -p docker -r eu-west-3 churn-serving
```

```bash
eb local run --port 9696
```
I get the following error:
ERROR: NotSupportedError - You can use "eb local" only with preconfigured, generic and multicontainer Docker platforms.  
Answer:
There are two options to fix this:
* Re-initialize by running eb init -i and choosing the options from a list (the first default option for docker platform should be fine). 
* Edit the ‘.elasticbeanstalk/config.yml’ directly changing the default_platform from Docker to default_platform: Docker running on 64bit Amazon Linux 2023

```bash
eb create churn-serving-env --enable-spot
```


## 5.9 Explore more

* Flask is not the only framework for creating web services. Try others, e.g. FastAPI
* Experiment with other ways of managing environment, e.g. virtual env, conda, poetry.
* Explore other ways of deploying web services, e.g. GCP, Azure, Heroku, Python Anywhere, etc

