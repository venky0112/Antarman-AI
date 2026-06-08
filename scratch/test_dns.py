import socket

try:
    print("Resolving huggingface.co...")
    ip1 = socket.gethostbyname("huggingface.co")
    print("huggingface.co IP:", ip1)
    
    print("Resolving api-inference.huggingface.co...")
    ip2 = socket.gethostbyname("api-inference.huggingface.co")
    print("api-inference.huggingface.co IP:", ip2)
except Exception as e:
    print("Error:", e)
