import numpy as np
import cv2
from cryptography.fernet import Fernet

def decrypt_image(encrypted_path, key_path, shape_path, output_image_path):
    with open(key_path, "rb") as f:
        key = f.read()

    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    shape = np.load(shape_path)
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    image_array = np.frombuffer(decrypted_data, dtype=np.uint8).reshape(shape)
    cv2.imwrite(output_image_path, image_array)
