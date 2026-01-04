import os
import uuid
import json
import redis
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = '/app/storage/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_QUEUE = 'image_resize_queue'

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Connect to Redis
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    r = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file temporarily
        try:
            file.save(save_path)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
        
        # Create job payload
        job = {
            'file_path': save_path,
            'filename': unique_filename,
            'target_size': (300, 300)
        }
        
        # Push to Redis queue
        if r:
            try:
                r.lpush(REDIS_QUEUE, json.dumps(job))
            except Exception as e:
                return jsonify({'error': f'Failed to enqueue job: {str(e)}'}), 500
        else:
             return jsonify({'error': 'Redis connection not available'}), 503

        return jsonify({
            'message': 'File uploaded and job queued successfully',
            'filename': unique_filename,
            'status': 'queued'
        }), 201
    
    return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed.'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    redis_status = 'connected'
    try:
        if r:
            r.ping()
        else:
            redis_status = 'disconnected'
    except:
        redis_status = 'error'
        
    return jsonify({'status': 'ok', 'redis': redis_status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
