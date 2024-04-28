from flask import Flask, render_template, request
import cv2
import numpy as np
import os
import base64

app = Flask(__name__)

class ImageProcessor:
    def process_image(self, image, operation):
        if operation == 'edge_detection':
            result = cv2.Canny(image, 100, 200)
        elif operation == 'color_inversion':
            result = cv2.bitwise_not(image)
        return result

image_processor = ImageProcessor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        operation = request.form['operation']
        image_files = request.files.getlist('images')
        processed_images = []
        for image in image_files:
            # Read the uploaded image
            nparr = np.fromstring(image.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the image
            processed_image = image_processor.process_image(img, operation)

            # Convert the processed image to base64 string
            retval, buffer = cv2.imencode('.jpg', processed_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            processed_images.append(img_base64)

        return render_template('results.html', processed_images=processed_images)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
