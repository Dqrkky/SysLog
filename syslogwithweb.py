import socket, json
from flask import Flask, jsonify

# Flask app setup
app = Flask(__name__)

# Shared variable to store received messages (simple example)
received_messages = []

# UDP Listener Function
def udp_listener(host :str="0.0.0.0", port :int=514):
    global received_messages
    # Set up UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port)) # Listen on all interfaces on port
    print(f"Listening for UDP messages on port {port}...")
    while True:
        message, addr = sock.recvfrom(4096)
        message = message.decode("Latin1")
        jsi = message.find('{')
        data = {
            "headers": message[:jsi],
            "data": json.loads(s=message[jsi:])
        }
        received_messages.append({"data": data, "address": addr})

# Flask Route to Display Received Messages
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(received_messages)

if __name__ == "__main__":
    # Start the UDP listener in a separate thread
    import threading
    listener_thread = threading.Thread(target=udp_listener, daemon=True)
    listener_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)  # Flask runs on HTTP port 5000
