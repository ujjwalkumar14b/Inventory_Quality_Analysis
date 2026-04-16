import os
from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

IMG_SIZE = (224, 224)
MODEL_PATH = "Inventory_Quality_Analysis.h5"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = tf.keras.models.load_model(MODEL_PATH)


def predict_image(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)[0][0]

    if pred > 0.5:
        return "Non-Defective"
    else:
        return "Defective"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    img_path = None

    if request.method == 'POST':
        file = request.files['file']

        if file:
            img_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(img_path)

            result = predict_image(img_path)

    return render_template('index.html', result=result, img_path=img_path)


if __name__ == '__main__':
    app.run(debug=True)

