import tensorflow_datasets as tfds

def get_breed_names():
    ds_info = tfds.builder('stanford_dogs').info
    breed_names = ds_info.features['label'].names
    return breed_names

def process_breed_name(breed):
    # Remove the prefix and split the name at underscores
    name_parts = breed[10:].split('_')
    
    # Capitalize the first letter of each part and join them with spaces
    readable_name = ' '.join([part.capitalize() for part in name_parts])
    
    return readable_name

def save_breed_names(breed_names, file_path='trained_model/breed_names.txt'):
    with open(file_path, 'w') as f:
        for breed in breed_names:
            readable_breed = process_breed_name(breed)
            f.write(f'{readable_breed}\n')

if __name__ == '__main__':
    breed_names = get_breed_names()
    save_breed_names(breed_names)
