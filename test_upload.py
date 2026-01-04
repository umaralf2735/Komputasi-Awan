import requests
import os

url = 'http://localhost:5000/upload'
files = {'file': open('Chibi_poses.jpg', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
