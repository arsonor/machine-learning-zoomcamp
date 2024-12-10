
## 10.3 Creating the pre-processing Flask service

In the previous section we created jupyter notebook to communicates with the model deployed with tensorflow. This notebook fetches an image, pre-process it, turns it into protobuf, sends it to tensorflow-serving, does post-processing, and finally gives a human-readable answer.

In this section we convert the notebook into python script to build flask application. To convert the notebook into script we can run the command `jupyter nbconvert --to script notebook.ipynb` and we rename the script to  [`gateway.py`](gateway.py).

Then we create functions to prepare request, send request, and prepare response. For flask app we can reuse the code from session 5:

```python
# Create flask app
app = Flask('gateway')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    url = data['url']
    result = predict(url)
    return jsonify(result)
```

Our application has two components: docker container with tensorflow serving and flask application with the gateway.

We also want to put everything in the `pipenv` for deployment. For that we need to install few libraries with pipenv: `pipenv install grpcio==1.42.0 flask gunicorn keras-image-helper`.

As we discussed tensorflow is a large library and we don't want to use it in our application. Instead we can use the following script to convert numpy array into protobuf format and import the `np_to_protobuf` function into our `gateway.py` script. In order the make the script work we need to install the following libraries as well `pipenv install tensorflow-protobuf==2.7.0 protobuf==3.19`:

```python
from tensorflow.core.framework import tensor_pb2, tensor_shape_pb2, types_pb2


def dtypes_as_dtype(dtype):
    if dtype == "float32":
        return types_pb2.DT_FLOAT
    raise Exception("dtype %s is not supported" % dtype)


def make_tensor_proto(data):
    shape = data.shape
    dims = [tensor_shape_pb2.TensorShapeProto.Dim(size=i) for i in shape]
    proto_shape = tensor_shape_pb2.TensorShapeProto(dim=dims)

    proto_dtype = dtypes_as_dtype(data.dtype)

    tensor_proto = tensor_pb2.TensorProto(dtype=proto_dtype, tensor_shape=proto_shape)
    tensor_proto.tensor_content = data.tostring()

    return tensor_proto


def np_to_protobuf(data):
    if data.dtype != "float32":
        data = data.astype("float32")
    return make_tensor_proto(data)
```

**Links**

- Bash script to create custom tf-serving-protobuf and compile: https://github.com/alexeygrigorev/tensorflow-protobuf/blob/main/tf-serving-proto.sh
