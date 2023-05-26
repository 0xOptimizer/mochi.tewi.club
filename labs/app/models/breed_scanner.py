import numpy as np
from tensorflow.keras.models import load_model
import tensorflow_hub as hub

def load_trained_model(model_path):
    return load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer})

def load_breed_names(file_path='trained_model/breed_names.txt'):
    with open(file_path, 'r') as f:
        breed_names = [line.strip() for line in f.readlines()]
    return breed_names

def predict_breed(image, model):
    prediction = model.predict(np.expand_dims(image, axis=0))
    breed = np.argmax(prediction)
    confidence = np.max(prediction) * 100  # Convert the probability to percentage
    return int(breed), confidence