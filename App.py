import os
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
import demucs.separate

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def process_file(filename):
    # set the working directory to the uploads folder
    os.chdir(app.config["UPLOAD_FOLDER"])
    # Execute the demucs command with the file path and name
    demucs.separate.main([os.path.join(UPLOAD_FOLDER, filename)])
    #command = f"demucs {os.path.join(UPLOAD_FOLDER, filename)}"
    #os.system(command)
    print(f"File processed: {filename}")

    # Notify the client that processing is complete
    with app.app_context():
        # Notify the client using a WebSocket, AJAX request, or any other suitable method
        # For simplicity, we'll use a global variable to store the processing status
        global is_processing
        is_processing = False

def get_files_recursively(directory):
    # Recursively get the list of files in a directory and its subdirectories
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, filename), start=directory))
    return files

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file to the UPLOAD_FOLDER
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Start processing the file in a separate thread
            thread = threading.Thread(target=process_file, args=(filename,))
            thread.start()

            return jsonify({'message': 'File uploaded and processing started.'})

    return render_template('index.html')

@app.route('/upload')
def upload_status():
    global is_processing
    if is_processing:
        return jsonify({'message': 'File is still processing. Please wait...'})
    else:
        return jsonify({'message': 'File processing is complete.'})

@app.route('/uploads')
def list_files():
    # Get the list of files in the uploads folder and its subdirectories
    files = get_files_recursively(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})

@app.route('/uploads/<path:filepath>')
def download_file(filepath):
    # Allow users to download a specific file from the uploads folder
    return send_from_directory(app.config['UPLOAD_FOLDER'], filepath)

if __name__ == '__main__':
    is_processing = False  # Global variable to track processing status
    app.run(debug=True)
