from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from encrypt import encrypt_image
from decrypt import decrypt_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        file = request.files.get('image_file')
        if not file:
            return "No image file uploaded", 400

        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Create encrypted folder inside static
        encrypted_folder = os.path.join('static', 'encrypted')
        os.makedirs(encrypted_folder, exist_ok=True)

        # Define encrypted output paths
        encrypted_path = os.path.join(encrypted_folder, f"encrypted_{filename}")
        key_path = os.path.join(encrypted_folder, f"{filename}_key.key")
        shape_path = os.path.join(encrypted_folder, f"{filename}_shape.npy")

        # Call encryption function
        encrypt_image(input_path, encrypted_path, key_path, shape_path)

        # Render result page
        return render_template('result.html',
                               action='Encryption',
                               image_name=filename,
                               encrypted_path=url_for('static', filename=f'encrypted/encrypted_{filename}'),
                               key_file=url_for('static', filename=f'encrypted/{filename}_key.key'),
                               shape_file=url_for('static', filename=f'encrypted/{filename}_shape.npy'))

    except Exception as e:
        return f"Error during encryption: {str(e)}", 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        encrypted_file = request.files.get('encrypted_file')
        key_file = request.files.get('key_file')
        shape_file = request.files.get('shape_file')

        if not encrypted_file or not key_file or not shape_file:
            return "One or more files are missing", 400

        encrypted_filename = secure_filename(encrypted_file.filename)
        key_filename = secure_filename(key_file.filename)
        shape_filename = secure_filename(shape_file.filename)

        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
        key_path = os.path.join(app.config['UPLOAD_FOLDER'], key_filename)
        shape_path = os.path.join(app.config['UPLOAD_FOLDER'], shape_filename)

        encrypted_file.save(encrypted_path)
        key_file.save(key_path)
        shape_file.save(shape_path)

        # Save decrypted image to static folder so it can be downloaded
        decrypted_folder = os.path.join('static', 'decrypted')
        os.makedirs(decrypted_folder, exist_ok=True)
        output_image_path = os.path.join(decrypted_folder, f"decrypted_{encrypted_filename}")

        decrypt_image(encrypted_path, key_path, shape_path, output_image_path)

        return render_template('result.html',
                               action='Decryption',
                               image_name=encrypted_filename,
                               encrypted_path=url_for('static', filename=f"decrypted/decrypted_{encrypted_filename}"),
                               key_file=None,
                               shape_file=None)
    except Exception as e:
        return f"Error during decryption: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
