# 🖼️ Distributed Image Resizer API

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

A scalable, distributed image resizing system built to handle high-concurrency image processing loads. It uses a producer-consumer architecture with **Flask** (API), **Redis** (Message Queue), and **Python Workers** (Processing), orchestrated via **Docker Compose**.

---

## 🚀 Features

*   **Distributed Architecture**: Decouples upload handling (API) from processing (Workers) using a message queue.
*   **Scalable Workers**: Scale the number of processing units horizontally with a single command.
*   **Web Interface**: Simple, user-friendly UI for uploading images.
*   **Local Storage Access**: Mapped volumes allow you to access uploaded and processed images directly from your host machine.
*   **Dockerized**: Fully containerized for easy deployment and isolation.

---

## 🏗️ Architecture

The system consists of three main components:

1.  **API Service**:
    *   Exposes a REST API (`POST /upload`) and a Web UI.
    *   Validates images and saves them to `storage/uploads`.
    *   Pushes a "Resize Job" to the Redis Queue.
2.  **Message Queue (Redis)**:
    *   Acts as a broker, distributing jobs to available workers.
3.  **Worker Service**:
    *   Constantly listens for new jobs.
    *   Resizes images to 300x300 pixels.
    *   Saves the result to `storage/processed`.

---

## 📦 Project Structure

```
project-root/
├── api/                # Flask API & UI
│   ├── app.py
│   ├── templates/
│   └── Dockerfile
├── worker/             # Background Worker
│   ├── worker.py
│   └── Dockerfile
├── storage/            # Persisted Data (Local)
│   ├── uploads/
│   └── processed/
├── docker-compose.yml  # Orchestration
├── load_test.py        # Stress Testing Script
└── README.md
```

---

## 🛠️ Getting Started

### Prerequisites

*   **Docker** & **Docker Compose** installed on your machine.

### Installation & Running

1.  **Clone the repository** (or navigate to the project folder):
    ```bash
    cd path/to/project
    ```

2.  **Start the application**:
    ```bash
    docker-compose up -d --build
    ```
    *This will start the API, Redis, and 3 Worker instances.*

3.  **Verify Status**:
    ```bash
    docker-compose ps
    ```
    Ensure all containers are `Up`.

---

## 💻 Usage

### 1. Web Interface (Recommended)
Open your browser and go to:
👉 **[http://localhost:5000](http://localhost:5000)**

Simply select a JPG/PNG file and click "Upload & Resize".

### 2. API Endpoint
You can also use `curl` or Postman:

```bash
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:5000/upload
```

### 3. Check Results
The processed images will appear in your local project folder:
📂 **`storage/processed/`**

---

## 🧪 Testing

### Load Testing (Concurrency)
To see the distributed system in action, we have provided a load testing script that sends 10 concurrent requests.

1.  Open a terminal to **monitor workers**:
    ```bash
    docker-compose logs -f worker
    ```

2.  Open another terminal to **run the test**:
    ```bash
    python load_test.py
    ```

Observe the logs in the first terminal—you will see different workers (`worker-1`, `worker-2`, `worker-3`) picking up jobs in parallel.

---

## ⚙️ Configuration

### Scalling Workers
Need more processing power? Scale the workers instantly:

```bash
docker-compose up -d --scale worker=5
```

---

## 📝 License
This project is created for **Komputasi Cloud - Tugas Besar**.
Free to use and modify for educational purposes.
