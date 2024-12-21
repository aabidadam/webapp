from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
import io
# Load pre-trained model
model_url = "https://tfhub.dev/google/imagenet/inception_v3/classification/5"
print("Loading model from URL:", model_url)
model = hub.load(model_url)
print("Model loaded successfully.")

labels_path = tf.keras.utils.get_file(
    "ImageNetLabels.txt",
    "https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt",
)
print("Downloading labels from URL.")
with open(labels_path, "r") as f:
    labels = [line.strip() for line in f.readlines()]
print("Labels loaded successfully.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def preprocess_image(image_data):
    """Preprocess the uploaded image for the model."""
    print("Preprocessing image.")
    try:
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        image = image.resize((299, 299))
        image_array = np.array(image) / 255.0
        preprocessed_image = np.expand_dims(image_array, axis=0).astype(np.float32)
        print("Image preprocessed successfully.")
        return preprocessed_image
    except Exception as e:
        print("Error in preprocessing image:", e)
        raise


def generate_description(image_data):
    """Generate a description for the uploaded image."""
    print("Generating description for the image.")
    preprocessed_image = preprocess_image(image_data)
    predictions = model(preprocessed_image).numpy()
    print("Model predictions:", predictions)
    predicted_index = np.argmax(predictions)
    description = labels[predicted_index]
    print("Predicted label:", description)
    return description


@app.route("/upload", methods=["POST"])
def upload_image():
    print("Received a request to upload image.")
    if "image" not in request.files:
        print("No image found in the request.")
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image_data = image_file.read()

    try:
        print("Processing uploaded image.")
        description = generate_description(image_data)
        print("Description generated successfully.")
        return jsonify({"description": description})
    except Exception as e:
        print("Error during image processing:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server.")
    app.run(debug=True)
