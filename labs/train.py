import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub

def load_stanford_dogs_dataset():
    (train_data, val_data), ds_info = tfds.load(
        'stanford_dogs',
        split=['train', 'test'],
        as_supervised=True,
        with_info=True,
    )
    return train_data, val_data, ds_info

def preprocess_image(image, label, img_size=224):
    image = tf.image.resize(image, (img_size, img_size))
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

def train_model(train_data, val_data, num_classes, epochs=10):
    train_data = train_data.map(preprocess_image).batch(32)
    val_data = val_data.map(preprocess_image).batch(32)

    feature_extractor = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/5"
    feature_extractor_layer = hub.KerasLayer(feature_extractor, input_shape=(224, 224, 3), trainable=False)

    model = tf.keras.Sequential([
        feature_extractor_layer,
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_data, epochs=epochs, validation_data=val_data)
    
    return model

def main():
    train_data, val_data, ds_info = load_stanford_dogs_dataset()
    num_classes = ds_info.features['label'].num_classes
    model = train_model(train_data, val_data, num_classes)
    model.save('trained_model/dog_breed_model.h5')

if __name__ == '__main__':
    main()
