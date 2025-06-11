import cv2
import numpy as np
from cryptography.fernet import Fernet
import os

def encrypt_image(input_image_path, encrypted_path, key_path, shape_path):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found or invalid.")

    image_bytes = image.tobytes()

    # Generate and save key
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)

    # Save image shape
    np.save(shape_path, image.shape)

    # Encrypt data
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(image_bytes)

    # Save encrypted binary
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)
