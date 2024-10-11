from flask import Flask, request, render_template_string
import cv2
import os

app = Flask(__name__)

# Enhanced cartoon effect function
def convert(image):
    # Step 1: Apply bilateral filter for smoothing while preserving edges
    color = cv2.bilateralFilter(image, d=9, sigmaColor=300, sigmaSpace=300)

    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply median blur to smooth the grayscale image
    gray = cv2.medianBlur(gray, 7)

    # Step 4: Use adaptive thresholding for edge detection
    edges = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, blockSize=9, C=2)

    # Step 5: Combine edges with color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartoon Effect</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
            }

            body {
                background: #e0e0e0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 20px 20px 60px #d9d9d9,
                            -20px -20px 60px #ffffff;
                padding: 20px;
                width: 90%;
                max-width: 400px;
                text-align: center;
            }

            h1 {
                margin-bottom: 20px;
                color: #333;
            }

            input[type="file"] {
                display: none;
            }

            label {
                background: #ffffff;
                border-radius: 12px;
                padding: 10px 20px;
                cursor: pointer;
                margin: 10px 0;
                display: inline-block;
                box-shadow: 8px 8px 30px #d9d9d9,
                            -8px -8px 30px #ffffff;
                transition: 0.3s;
            }

            label:hover {
                box-shadow: 4px 4px 20px #d9d9d9,
                            -4px -4px 20px #ffffff;
            }

            button {
                background: #4CAF50;
                border: none;
                border-radius: 12px;
                color: white;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                box-shadow: 8px 8px 30px #d9d9d9,
                            -8px -8px 30px #ffffff;
                transition: 0.3s;
                margin: 10px 0;
            }

            button:hover {
                background: #45a049;
            }

            .result-image {
                margin-top: 20px;
                display: none;
            }

            @media (max-width: 600px) {
                .container {
                    width: 95%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Upload Image for Cartoon Effect</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <label for="file"><i class="fas fa-upload"></i> Choose File</label>
                <input type="file" name="file" id="file" accept="image/*" required>
                <button type="submit">Upload</button>
            </form>
            <div class="result-image">
                <h2>Cartoon Image:</h2>
                <img id="cartoon-image" src="" alt="Cartoon Image" style="max-width: 100%;">
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template_string('<h1>Error: No file uploaded</h1>'), 400

    file = request.files['file']
    if file.filename == '':
        return render_template_string('<h1>Error: No file selected</h1>'), 400

    # Read the image file into a numpy array
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    image = cv2.imread(file_path)

    # Apply the cartoon effect
    cartoon_image = convert(image)

    # Save the cartoon image
    cartoon_file_path = os.path.join('static', 'cartoon_' + file.filename)
    cv2.imwrite(cartoon_file_path, cartoon_image)

    # Return the HTML page with the cartoon image URL
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartoon Effect Result</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
            }

            body {
                background: #e0e0e0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 20px 20px 60px #d9d9d9,
                            -20px -20px 60px #ffffff;
                padding: 20px;
                width: 90%;
                max-width: 400px;
                text-align: center;
            }

            h1 {
                margin-bottom: 20px;
                color: #333;
            }

            img {
                max-width: 100%;
                border-radius: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Cartoon Effect Applied!</h1>
            <img src="/static/{{ cartoon_image }}" alt="Cartoon Image">
            <a href="/">Go Back</a>
        </div>
    </body>
    </html>
    ''', cartoon_image='cartoon_' + file.filename)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5002)  # Make the app accessible on all interfaces
            }

            button {
                background: #4CAF50;
                border: none;
                border-radius: 12px;
                color: white;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 16px;
                box-shadow: 8px 8px 30px #d9d9d9,
                            -8px -8px 30px #ffffff;
                transition: 0.3s;
                margin: 10px 0;
            }

            button:hover {
                background: #45a049;
            }

            .result-image {
                margin-top: 20px;
                display: none;
            }

            @media (max-width: 600px) {
                .container {
                    width: 95%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Upload Image for Cartoon Effect</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <label for="file"><i class="fas fa-upload"></i> Choose File</label>
                <input type="file" name="file" id="file" accept="image/*" required>
                <button type="submit">Upload</button>
            </form>
            <div class="result-image">
                <h2>Cartoon Image:</h2>
                <img id="cartoon-image" src="" alt="Cartoon Image" style="max-width: 100%;">
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template_string('<h1>Error: No file uploaded</h1>'), 400

    file = request.files['file']
    if file.filename == '':
        return render_template_string('<h1>Error: No file selected</h1>'), 400

    # Read the image file into a numpy array
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    image = cv2.imread(file_path)

    # Apply the cartoon effect
    cartoon_image = convert(image)

    # Save the cartoon image
    cartoon_file_path = os.path.join('static', 'cartoon_' + file.filename)
    cv2.imwrite(cartoon_file_path, cartoon_image)

    # Return the HTML page with the cartoon image URL
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartoon Effect Result</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
            }

            body {
                background: #e0e0e0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .container {
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 20px 20px 60px #d9d9d9,
                            -20px -20px 60px #ffffff;
                padding: 20px;
                width: 90%;
                max-width: 400px;
                text-align: center;
            }

            h1 {
                margin-bottom: 20px;
                color: #333;
            }

            img {
                max-width: 100%;
                border-radius: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Cartoon Effect Applied!</h1>
            <img src="/static/{{ cartoon_image }}" alt="Cartoon Image">
            <a href="/">Go Back</a>
        </div>
    </body>
    </html>
    ''', cartoon_image='cartoon_' + file.filename)

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5002)  # Make the app accessible on all interfaces
