import cv2 as cv
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image
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
    
send("command")
receive()
send("streamon")
receive()

# Set up video capture from webcam
# Get the video stream from Tello on port 11111
cam = cv.VideoCapture('udp://127.0.0.1:11111')


while True:
    #Read a camera frame
    ret_val,img = cam.read()
    #img = imutils.resize(img, width=400)
    if img is not None:
        img = cv.flip(img,1)
        
        #Detect markers
        img, marker_details = detect_markers_in_image(img,
                                                      draw_center = True,
                                                      draw_reference_corner = True,
                                                      target_id = None,
                                                      draw_target_id=True,
                                                      draw_border=True)
        #Print marker details
        for marker_detail in marker_details:
            print("Marker ID: " + str(marker_detail[1]))
            print("Marker position: "+str(marker_detail[0]))
            if marker_detail[1] == 512:
                send("takeoff")
                receive()
            elif marker_detail[1] == 128:
                send("land")
                receive()
            elif marker_detail[1] == 728:
                send("flip f")
                receive()
        #Image display
        cv.imshow('Original webcam image',img)

        #Check for key presses
        pressedKey = cv.waitKey(1)
        if pressedKey == 27:
            break

    
# Close the UDP socket
sock.close()

