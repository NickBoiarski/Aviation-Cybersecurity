import socket

#Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Address 0.0.0.0 allows connections from anywhere
sock.bind(('0.0.0.0', 12345))

#Listen for a connection
sock.listen(1)

#Waiting for connection
print("Waiting for connection")

client_socket, client_address = sock.accept()

print(f"Connection from {client_address}")

#Until interrupt print received telemetry
while True:

    data = client_socket.recv(1024)

    print(f"Received telemetry: {data.decode()}") 