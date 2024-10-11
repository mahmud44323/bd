from flask import Flask, request, jsonify
import cv2
import os

app = Flask(__name__)

# Function to apply cartoon effect
def convert(image):
    Gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    Blur_image = cv2.GaussianBlur(Gray_image, (3, 3), 0)
    detect_edge = cv2.adaptiveThreshold(Blur_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)
    output = cv2.bitwise_and(image, image, mask=detect_edge)
    return output

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartoon Effect</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            /* Styles here... */
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Upload Image for Cartoon Effect</h1>
            <form id="uploadForm" enctype="multipart/form-data">
                <label for="file"><i class="fas fa-upload"></i> Choose File</label>
                <input type="file" name="file" id="file" accept="image/*" required>
                <button type="submit">Upload</button>
            </form>
            <div id="previewContainer" style="display: none;">
                <h2>Cartooned Image Preview</h2>
                <img id="previewImage" src="" alt="Cartooned Image" style="max-width: 100%;">
            </div>
        </div>

        <script>
            document.getElementById('uploadForm').onsubmit = async function(event) {
                event.preventDefault();
                const fileInput = document.getElementById('file');
                const file = fileInput.files[0];

                if (!file) return;

                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                if (result.cartoon_image_url) {
                    document.getElementById('previewImage').src = result.cartoon_image_url;
                    document.getElementById('previewContainer').style.display = 'block';
                } else {
                    alert('Failed to apply cartoon effect.');
                }
            };
        </script>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Read and convert the image
    image = cv2.imread(file_path)
    cartoon_image = convert(image)
    
    # Save the cartooned image
    cartoon_file_path = os.path.join('static', 'cartoon_' + file.filename)
    cv2.imwrite(cartoon_file_path, cartoon_image)

    return jsonify({"cartoon_image_url": f"/{cartoon_file_path}"}), 200

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5002)
