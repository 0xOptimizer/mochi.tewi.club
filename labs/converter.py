import tensorflow as tf
import tensorflow_hub as hub

# Load your existing model
model = tf.keras.models.load_model('trained_model/dog_breed_model.h5', custom_objects={'KerasLayer': hub.KerasLayer})

# Convert the model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the converted model to a .tflite file
with open('trained_model/dog_breed_model.tflite', 'wb') as f:
    f.write(tflite_model)