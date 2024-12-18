## 10.2 TensorFlow Serving

To build the app we need to convert the keras model `HDF5` into special format called tensorflow `SavedModel`. To do that, we download a prebuilt model and save it in the working directory:

```bash
wget https://github.com/DataTalksClub/machine-learning-zoomcamp/releases/download/chapter7-model/xception_v4_large_08_0.894.h5 -O clothing-model.h5
```

Then convert the model to `SavedModel` format:

```python
import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('./clothing-model.h5')

tf.saved_model.save(model, 'clothing-model')
```

We can inspect what's inside the saved model using the utility (saved_model_cli) from TensorFlow and the following command:
```shell
saved_model_cli show --dir clothing-model --all
```

Running the command outputs a few things but we are interested in the signature, specifically the following one. For instance:

```bash
signature_def['serving_default']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['input_8'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 299, 299, 3)
        name: serving_default_input_8:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['dense_7'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 10)
        name: StatefulPartitionedCall:0
  Method name is: tensorflow/serving/predict
```
Alternatively one can also use the following command to output just the desired part:
```shell
saved_model_cli show --dir clothing-model --tag_set serve --signature_def serving_default
```

We can run the model (`clothing-model`) with the prebuilt docker image `tensorflow/serving:2.7.0`:

```bash
docker run -it --rm \
  -p 8500:8500 \
  -v $(pwd)/clothing-model:/models/clothing-model/1 \
  -e MODEL_NAME="clothing-model" \
  tensorflow/serving:2.7.0
```

- docker run -it --rm (to run the docker)
- -p 8500:8500 (port mapping)
- -v $(pwd)/clothing-model:/models/clothing-model/1 (volume mapping of *absolute model directory* to *model directory inside the docker image*)
- -e MODEL_NAME="clothing-model" (set environment variable for docker image)
- tensorflow/serving:2.7.0 (name of the image to run)

Tensorflow uses special serving called `gRPC` protocol which is optimized to use binary data format. We need to convert our prediction into `protobuf`.

See the code here: [tf-serving-connect.ipynb](tf-serving-connect.ipynb)
