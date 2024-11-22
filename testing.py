import socket

try:
    socket.create_connection(("smtp.gmail.com", 587), timeout=10)
    print("Connection to port 587 successful")
except Exception as e:
    print(f"Connection to port 587 failed: {e}")

try:
    socket.create_connection(("smtp.gmail.com", 465), timeout=10)
    print("Connection to port 465 successful")
except Exception as e:
    print(f"Connection to port 465 failed: {e}")