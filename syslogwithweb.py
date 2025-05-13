import socket
import json
import threading
import queue
from flask import Flask, jsonify, Response

app = Flask(__name__)

# Thread-safe queue to store incoming messages
message_queue = queue.Queue()
message_history = []

def udp_listener(host="0.0.0.0", port=514):
    """Listens for incoming UDP messages and puts them in a queue."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Listening for UDP messages on port {port}...")
    while True:
        message, addr = sock.recvfrom(4096)
        message = message.decode("Latin1")
        jsi = message.find('{')
        data = {
            "headers": message[:jsi],
            "data": json.loads(message[jsi:])
        }
        entry = {"data": data, "address": addr}
        message_queue.put(entry)
        message_history.append(entry)

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(message_history)

def event_stream():
    """Generator function to stream messages in real time."""
    while True:
        message = message_queue.get()
        yield f"data: {json.dumps(message)}\n\n"

@app.route('/stream', methods=['GET'])
def stream():
    """SSE endpoint for real-time message streaming."""
    return Response(event_stream(), content_type='text/event-stream')

if __name__ == "__main__":
    # Start UDP listener in a separate thread
    listener_thread = threading.Thread(target=udp_listener, daemon=True)
    listener_thread.start()

    # Run Flask app
    app.run(host="0.0.0.0", port=5000, threaded=True)
