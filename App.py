import os
import threading
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def process_file(filename):
    # Execute the demucs command with the file path and name
    command = f"demucs {os.path.join(UPLOAD_FOLDER, filename)}"
    os.system(command)
    print(f"File processed: {filename}")

    # Notify the client that processing is complete
    with app.app_context():
        # Notify the client using a WebSocket, AJAX request, or any other suitable method
        # For simplicity, we'll use a global variable to store the processing status
        global is_processing
        is_processing = False


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


if __name__ == '__main__':
    is_processing = False  # Global variable to track processing status
    app.run(debug=True)