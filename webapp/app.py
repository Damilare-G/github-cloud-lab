from flask import Flask, jsonify
import os
import socket
import redis

app = Flask(__name__)

# Connect to Redis (service name 'redis' resolves inside Docker network)
cache = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379)


@app.route("/")
def index():
    try:
        visits = cache.incr("visits")
    except Exception:
        visits = "unavailable"

    return (
        "<h1>GitHub Cloud Lab</h1>"
        f"<p>This page has been visited <strong>{visits}</strong> times.</p>"
    )


@app.route("/info")
def info():
    return jsonify({
        "hostname": socket.gethostname(),
        "environment": os.environ.get("APP_ENV", "development"),
    })
