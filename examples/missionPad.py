import socket
import time

# IP and port of Tello
tello_address = ('192.168.10.1', 8889)

# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Let's be explicit and bind to a local port on our machine where Tello can send messages
sock.bind(('', 9000))

# Function to send messages to Tello
def send(message):
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

# Function that listens for messages from Tello and prints them to the screen
def receive():
  try:
    response, ip_address = sock.recvfrom(128)
    print("Received message: " + response.decode(encoding='utf-8') + " from Tello with IP: " + str(ip_address))
  except Exception as e:
    print("Error receiving: " + str(e))

# You will start here
# Send Tello into command mode
send("command")
# Receive response from Tello
receive()

# Enable mission pad
send("mon")
receive()

send("takeoff")
receive()
send("go 50 50 120 50 m8")
receive()
send("go -50 50 120 50 m8")
receive()
send("go -50 -50 120 50 m8")
receive()
send("go 50 -50 120 50 m8")
receive()
send("go 0 0 50 50 m8")
receive()
send("land")
receive()



# Close the UDP socket
sock.close()
