import os
import socket
import ssl



#Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#PKI verification
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH) #CLIENT_AUTH makes a certificate required

context.load_cert_chain(certfile='/home/drone-controller/Desktop/certificates/server.crt', keyfile='/home/drone-controller/Desktop/certificates/server.key') #Change to required directory

context.load_verify_locations(cafile='/home/drone-controller/Desktop/certificates/ca.pem') #Change to required directory

#Applies TLS encryption
wrapped_socket = context.wrap_socket(sock, server_side=True)

#Bind socket to address and port
# Address 0.0.0.0 allows connections from anywhere
wrapped_socket.bind(('0.0.0.0', 12345))

#Listen for a connection
wrapped_socket.listen(1)

while True:

    print("Waiting for connection")
    client_socket, client_address = wrapped_socket.accept()
    print(f"Connection from {client_address}")

    pid = os.fork()

    if pid == 0:  #Child

        drone_name = client_socket.recv(1024).decode('utf-8')  # Receive drone name first

        print(f"Drone Name: {drone_name}")

        #Until interrupt print received telemetry
        while True:

            data = client_socket.recv(1024)

            print(f"{drone_name}: {data.decode()}")

        client_socket.close()

        os._exit(0)  #Terminal the child

    else:  #Parent sent here

        client_socket.close()  # Close the client socket in the parent process