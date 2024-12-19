# Backend: Flask with TensorFlow Hub
from flask import Flask, request, jsonify
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
import io


# Load pre-trained model
model_url = "https://tfhub.dev/google/imagenet/inception_v3/classification/5"
model = hub.load(model_url)
labels_path = tf.keras.utils.get_file(
    'ImageNetLabels.txt',
    'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt'
)
with open(labels_path, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Initialize Flask app
app = Flask(__name__)

def preprocess_image(image_data):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    image = image.resize((299, 299))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)

def generate_description(image_data):
    preprocessed_image = preprocess_image(image_data)
    predictions = model(preprocessed_image)
    predicted_index = np.argmax(predictions)
    return labels[predicted_index]

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image_data = image_file.read()
    
    try:
        description = generate_description(image_data)
        return jsonify({"description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
