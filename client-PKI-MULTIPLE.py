import socket
import ssl
from pymavlink import mavutil

#Use MAVLink to connect to the Gazebo simulation
mavlink_connection = mavutil.mavlink_connection('udp:localhost:14550')

#Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#PKI verification
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH) #SERVER_AUTH makes a certificate required

context.load_cert_chain(certfile='/home/drone-vm/Desktop/certificates/client.crt', keyfile='/home/drone-vm/Desktop/certificates/client.key') #Change these to required directory

context.load_verify_locations(cafile='/home/drone-vm/Desktop/certificates/ca.pem') #Change to required directory

#Applies TLS encryption
wrapped_socket = context.wrap_socket(sock, server_hostname='drone-controller') #Using IP as hostname causes issues so add to /etc/hosts

#This connects to the server
wrapped_socket.connect(('drone-controller', 12345))

#Send drone name
drone_name = "drone1"  #Change for each drone used

wrapped_socket.sendall(drone_name.encode()) #Need to send a string over the socket

#Keep sending telemetry until interrupt
while True:

    msg = mavlink_connection.recv_match(type='GLOBAL_POSITION_INT')  # From MAVLink website, gives alt, spd, lat, lon

    #msg is sometimes empty which can cause errors
    if msg is not None:

        #set the values to human readable values
        altitude = msg.relative_alt / 1000
        speed = msg.vx / 100
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7

        data = f"Altitude: {altitude} meters, Speed: {speed} m/s, Lat: {lat}, Lon: {lon}"

        wrapped_socket.sendall(data.encode())
