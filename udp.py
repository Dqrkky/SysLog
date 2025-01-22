import socket
import time

target_ip = "localhost"
target_port = 514
message = "PING"

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)
 
sock.settimeout(10)
 
while True:
    data = (
        message.encode("utf-8"),
        (target_ip, target_port)
    )
    print(data)
    if isinstance(data[0], bytes):
        sock.sendto(*data)
    time.sleep(0.5)