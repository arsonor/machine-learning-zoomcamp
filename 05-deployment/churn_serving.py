import pickle

from flask import Flask, request, jsonify

def predict_single(customer, dv, model):
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]


with open('churn-model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


app = Flask('churn')


@app.route('/predict', methods=['POST']) ## in order to send the customer information we need to post its data.
def predict():
    customer = request.get_json() ## web services work best with json frame, So after the user post its data in json format we need to access the body of json.

    prediction = predict_single(customer, dv, model)
    churn = prediction >= 0.5
    
    result = {
        'churn_probability': float(prediction), ## we need to cast numpy float type to python native float type
        'churn': bool(churn), ## same as the line above, casting the value using bool method
    }

    return jsonify(result)  ## send back the data in json format to the user


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)