import numpy as np
from PIL import Image
from flask_mail import Message
from .main import mail

def preprocess_image(image_file):
    image = Image.open(image_file)
    image = image.resize((224, 224))  # Resize the image to 224x224
    image = image.convert('RGB')  # Convert the image to RGB format
    return np.array(image) / 255.0  # Normalize pixel values

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=('Your Name', 'your@email.com')
    )
    mail.send(msg)