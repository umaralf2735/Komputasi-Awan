import os
import json
import time
import redis
from PIL import Image

# Configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_QUEUE = 'image_resize_queue'
PROCESSED_FOLDER = '/app/storage/processed'

# Ensure processed directory exists
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def resize_image(file_path, filename, target_size):
    try:
        with Image.open(file_path) as img:
            img = img.resize(target_size)
            output_path = os.path.join(PROCESSED_FOLDER, filename)
            img.save(output_path)
            print(f"Successfully resized {filename} to {target_size}")
            return True
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False

def main():
    print("Worker started. Connecting to Redis...")
    
    # Retry connection logic
    while True:
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
            r.ping()
            print("Connected to Redis successfully.")
            break
        except redis.ConnectionError:
            print("Redis not available, retrying in 5 seconds...")
            time.sleep(5)

    print(f"Listening on queue: {REDIS_QUEUE}")
    
    while True:
        # Blocking pop from Redis list
        # timeout=0 means block indefinitely
        task = r.blpop(REDIS_QUEUE, timeout=0)
        
        if task:
            # task is a tuple (queue_name, data)
            queue_name, data = task
            try:
                job = json.loads(data)
                print(f"Received job: {job}")
                
                file_path = job.get('file_path')
                filename = job.get('filename')
                target_size = tuple(job.get('target_size', (300, 300)))
                
                if os.path.exists(file_path):
                    resize_image(file_path, filename, target_size)
                else:
                    print(f"File not found: {file_path}")
                    
            except json.JSONDecodeError:
                print("Error decoding job data")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
