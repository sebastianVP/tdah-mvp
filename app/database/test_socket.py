# test_socket.py

import socket

s = socket.socket()

try:
    s.connect(("127.0.0.1", 5432))
    print("✅ Puerto 5432 accesible")
except Exception as e:
    print("❌ Error:", e)

s.close()