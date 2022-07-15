# This example script demonstrates how to use Python to fly Tello in a box mission with a loop
# This script is part of our course on Tello drone programming
# https://learn.droneblocks.io/p/tello-drone-programming-with-python/

# Import the necessary modules
import socket
import threading
import time

# IP and port of Tello
tello1 = ('192.168.0.145', 8889)
tello2 = ('192.168.0.169', 8889)
tello3 = ('192.168.0.123', 8889)

# IP and port of local computer
local_address = ('', 9000)

# Create a UDP connection that we'll send the command to
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock.bind(local_address)

# Send the message to Tello and allow for a delay in seconds
def send(message, drone):
  # Try to send the message otherwise print the exception
  try:
    sock.sendto(message.encode(), drone)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))


# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response, ip_address = sock.recvfrom(128)
      print("Received message: " + response.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()


#Your code starts here
# Put Tello into command mode
send("command", tello1)
send("command", tello2)
send("command", tello3)
time.sleep(5)

# Send the takeoff command
send("takeoff", tello1)
send("takeoff", tello2)
send("takeoff", tello3)
time.sleep(7)

send("up 100", tello1)
send("up 100", tello2)
send("up 100", tello3)
time.sleep(7)

send("up 50", tello1)
send("down 50", tello2)
send("up 50", tello3)
time.sleep(5)

send("up 50", tello1)
send("down 50", tello2)
send("up 50", tello3)
time.sleep(5)


send("flip f", tello1)
time.sleep(1)
send("flip f", tello2)
time.sleep(1)
send("flip f", tello3)
time.sleep(1)

# Land
send("land", tello1)
send("land", tello2)
send("land", tello3)

# Print message
print("Mission completed successfully!")

# Close the socket
sock.close()
