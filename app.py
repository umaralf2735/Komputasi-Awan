from flask import Flask, jsonify, render_template
import redis
import os
import socket

app = Flask(__name__)

# Menggunakan Redis, host='redis' sesuai nama service di docker-compose
# port=6379 adalah default Redis
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route("/")
def index():
    # Menampilkan hostname container untuk membuktikan load balancing
    hostname = socket.gethostname()
    return render_template("index.html", hostname=hostname)

@app.route("/counter", methods=["GET"])
def get_counter():
    # Mengambil nilai counter dari Redis (key: 'counter')
    value = r.get("counter")
    
    # Jika belum ada nilai, inisialisasi dengan 0
    if value is None:
        value = 0
    
    return jsonify({"counter": value})

@app.route("/counter/increment", methods=["POST"])
def increment_counter():
    # Atomic increment di Redis
    new_value = r.incr("counter")
    return jsonify({"counter": new_value})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
