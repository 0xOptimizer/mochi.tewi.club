import os
import cv2
import numpy as np
import pandas as pd
import zipfile
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
import urllib.request
import ast
import re

def sanitize_filename(filename):
    return re.sub(r'[?=&]', '_', filename)

def download_image(url, save_path):
    try:
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return False

def load_cat_breeds_dataset(cats_csv='cats.csv', downloaded_images_dir='downloaded_images'):
    if not os.path.exists(downloaded_images_dir):
        os.makedirs(downloaded_images_dir)

    # Load the csv file with image URLs and their corresponding labels
    labels_df = pd.read_csv(cats_csv)

    images = []
    labels = []

    label_mapping = {label: idx for idx, label in enumerate(labels_df['breed'].unique())}
    for idx, row in labels_df.iterrows():
        med_photos = ast.literal_eval(row['med_photos'])  # Convert the string representation of a list to an actual list
        for url in med_photos:
            file_name = sanitize_filename(url.split('/')[-1])
            save_path = os.path.join(downloaded_images_dir, file_name)

            if not os.path.exists(save_path):
                if not download_image(url, save_path):
                    continue

            image = cv2.imread(save_path)
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                images.append(image)
                labels.append(label_mapping[row['breed']])

    images = np.array(images)
    labels = np.array(labels)

    train_data, val_data, train_labels, val_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

    train_data = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
    val_data = tf.data.Dataset.from_tensor_slices((val_data, val_labels))

    return train_data, val_data, label_mapping

def main():
    train_data, val_data, label_mapping = load_cat_breeds_dataset()
    num_classes = len(label_mapping)
    model = train_model(train_data, val_data, num_classes)
    model.save('trained_model/cat_breed_model.h5')

if __name__ == '__main__':
    main()