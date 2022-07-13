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

def squareOne():
  send("forward 280")
  receive()
  send("ccw 90")
  receive()
  send("forward 228")
  receive()
  send("ccw 90")
  receive()
  send("forward 240")
  receive()
  send("ccw 90")
  receive()
  send("forward 250")
  receive()
  send("ccw 90")
  receive()

def squareTwo():
  speed = 70
  send("go 280 0 0 "+str(speed))
  receive()
  send("go 0 228 0 "+str(speed))
  receive()
  send("go -240 0 0 "+str(speed))
  receive()
  send("go 0 -250 0 "+str(speed))
  receive()

def squareThree():
  speed = 50
  send("curve 140 45 0 280 0 0 "+str(speed))
  receive()
  send("curve 45 114 0 0 228 0 "+str(speed))
  receive()
  send("curve -120 45 0 -240 0 0 "+str(speed))
  receive()
  send("curve -45 -125 0 0 -250 0 "+str(speed))
  receive()
  
# Send Tello into command mode
send("command")
# Receive response from Tello
receive()

# Delay 3 seconds before we send the next command
time.sleep(3)

# Ask Tello about battery status
send("battery?")
# Receive battery response from Tello
receive()

send("takeoff")
receive()

# Exercise 1 - fly square without command restrictions
squareOne()
# Exercise 2 - fly square using go command
squareTwo()
# Exercise 3 - fly square using curve command
squareThree()

# Exercise 4
laps=input("How many laps would you like to fly?")
print("Ok. I will fly "+str(laps)+" laps")
for i in range(laps):
  squareOne()

# Exercise 5
userInput = input("Which exercise would you like to fly (1,2,3)?")
laps=input("How many laps would you like to fly?")
print("Ok. I will fly "+str(laps)+" laps")
if userInput == 1:
  for i in range(laps):
    squareOne()
elif userInput == 2:
  for i in range(laps):
    squareTwo()
else:
  for i in range(laps):
    squareThree()
    
# Close the UDP socket
sock.close()
