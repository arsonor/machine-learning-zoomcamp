import requests

# url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
url = 'https://695o0rt9j8.execute-api.eu-west-3.amazonaws.com/test/predict'

data = {'url': 'http://bit.ly/mlbookcamp-pants'}

result = requests.post(url, json=data).json()
print(result)