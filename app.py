import cv2
import numpy as np
from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_image', methods=['POST'])
def process_image():

    if 'image' not in request.files:
        return render_template(
            'index.html',
            error="No image selected."
        )

    image_file = request.files['image']

    if image_file.filename == '':
        return render_template(
            'index.html',
            error="Please upload an image."
        )

    image_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        image_file.filename
    )

    image_file.save(image_path)

    image = cv2.imread(image_path)

    if image is None:
        return render_template(
            'index.html',
            error="Invalid image format."
        )

    b, g, r = cv2.split(image)

    result = {
        'image_path': image_path,

        'b_min': int(np.min(b)),
        'b_max': int(np.max(b)),
        'b_mean': round(float(np.mean(b)), 2),
        'b_var': round(float(np.var(b)), 2),

        'g_min': int(np.min(g)),
        'g_max': int(np.max(g)),
        'g_mean': round(float(np.mean(g)), 2),
        'g_var': round(float(np.var(g)), 2),

        'r_min': int(np.min(r)),
        'r_max': int(np.max(r)),
        'r_mean': round(float(np.mean(r)), 2),
        'r_var': round(float(np.var(r)), 2)
    }

    return render_template(
        'results.html',
        **result
    )


if __name__ == "__main__":
    app.run(debug=True)