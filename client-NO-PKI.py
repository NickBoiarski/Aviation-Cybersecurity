import socket
from pymavlink import mavutil

#Use MAVLink to connect to the Gazebo simulation
mavlink_connection = mavutil.mavlink_connection('udp:localhost:14550')

#Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#This connects to the server
sock.connect(('drone-controller', 12345))

#Keep sending telemetry until interrupt
while True:

    msg = mavlink_connection.recv_match(type='GLOBAL_POSITION_INT')  # From MAVLink website, gives alt, spd, lat, lon

    #msg is sometimes empty which can cause errors
    if msg is not None:

        altitude = msg.relative_alt / 1000
        speed = msg.vx / 100
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7

        data = f"Altitude: {altitude} meters, Speed: {speed} m/s, Lat: {lat}, Lon: {lon}"

        sock.sendall(data.encode())