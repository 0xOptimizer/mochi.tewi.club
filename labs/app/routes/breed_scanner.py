import tensorflow as tf

from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
from ..models.breed_scanner import load_trained_model, predict_breed, load_breed_names
from ..utils import preprocess_image

breed_scanner_bp = Blueprint('breed_scanner', __name__, url_prefix='/')
CORS(breed_scanner_bp)

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

model = load_trained_model('trained_model/dog_breed_model.h5')
breed_names = load_breed_names()

@breed_scanner_bp.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['file']
    image = preprocess_image(image_file)
    breed, confidence = predict_breed(image, model)
    readable_breed = breed_names[breed]

    return jsonify({'breed': breed, 'readable_breed': readable_breed, 'confidence': confidence}), 200