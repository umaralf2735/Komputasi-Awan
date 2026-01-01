import requests
import concurrent.futures
import time
import os

URL = 'http://localhost:5000/upload'
IMAGE_PATH = 'test_image.jpg'
CONCURRENT_REQUESTS = 10

def upload_image(i):
    try:
        with open(IMAGE_PATH, 'rb') as f:
            files = {'file': f}
            start_time = time.time()
            response = requests.post(URL, files=files)
            duration = time.time() - start_time
            print(f"Request {i}: Status {response.status_code} - {duration:.2f}s")
            return response.text
    except Exception as e:
        print(f"Request {i} failed: {e}")

def main():
    print(f"Starting load test with {CONCURRENT_REQUESTS} concurrent uploads...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(upload_image, i) for i in range(CONCURRENT_REQUESTS)]
        
        for future in concurrent.futures.as_completed(futures):
            future.result()
            
    total_duration = time.time() - start_time
    print(f"\nAll requests completed in {total_duration:.2f}s")

if __name__ == "__main__":
    if not os.path.exists(IMAGE_PATH):
        # Create dummy image if not exists
        from PIL import Image
        img = Image.new('RGB', (1000, 1000), color = 'blue')
        img.save(IMAGE_PATH)
        
    main()
