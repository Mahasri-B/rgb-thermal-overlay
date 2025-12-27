from flask import Flask, request, send_file, render_template, jsonify
import io
import os
import cv2
import numpy as np

from overlay_thermal import align_thermal_to_rgb

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/align', methods=['POST'])
def align():
    try:
        if 'thermal' not in request.files or 'rgb' not in request.files:
            return jsonify({'error': 'Please upload both files (thermal and rgb)'}), 400

        th_file = request.files['thermal']
        rgb_file = request.files['rgb']

        if th_file.filename == '' or rgb_file.filename == '':
            return jsonify({'error': 'Please select both files'}), 400

        # Read images into OpenCV
        th_bytes = th_file.read()
        rgb_bytes = rgb_file.read()
        th_arr = np.frombuffer(th_bytes, np.uint8)
        rgb_arr = np.frombuffer(rgb_bytes, np.uint8)
        thermal = cv2.imdecode(th_arr, cv2.IMREAD_COLOR)
        rgb = cv2.imdecode(rgb_arr, cv2.IMREAD_COLOR)

        if thermal is None or rgb is None:
            return jsonify({'error': 'Failed to decode one of the uploaded images. Please ensure both are valid image files.'}), 400

        # Align
        aligned = align_thermal_to_rgb(thermal, rgb)

        # Encode aligned thermal to JPG bytes
        ok, aligned_jpg = cv2.imencode('.JPG', aligned)
        if not ok:
            return jsonify({'error': 'Failed to encode output image'}), 500

        # Return only the aligned thermal image as JPG
        return send_file(
            io.BytesIO(aligned_jpg.tobytes()),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='aligned_AT.JPG'
        )
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
