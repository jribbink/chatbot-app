import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import random
import pickle
import json


class NeuralNet:
    def __init__(self):
        with open("config/dataset.json") as file:
            self.data = json.load(file)

    def queryNN(self, input):
        # load trained model
        model = keras.models.load_model("chat_model")

        # load tokenizer object
        with open("tokenizer.pickle", "rb") as handle:
            tokenizer = pickle.load(handle)

        # load label encoder object
        with open("label_encoder.pickle", "rb") as enc:
            lbl_encoder: LabelEncoder = pickle.load(enc)

        # parameters
        max_len = 20

        result: np.array = model.predict(
            keras.preprocessing.sequence.pad_sequences(
                tokenizer.texts_to_sequences([input]), truncating="post", maxlen=max_len
            )
        )
        intent_key = lbl_encoder.inverse_transform([np.argmax(result)])[0]

        # Check if phrase is not highly recognizable (similar to default)
        label_index = lbl_encoder.transform(np.array(["default"]))
        default_weight = result[0][label_index]
        if default_weight > 0.001:
            intent_key = "default"

        # print(sorted((r,i) for (_,i), r in np.ndenumerate(result)))

        return random.choice(self.data[intent_key]["responses"])
