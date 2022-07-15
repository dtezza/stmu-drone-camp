import cv2 as cv
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center
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
max_speed=100
min_distance = 20

send("takeoff")
receive()
while True:
    #Read a camera frame
    ret_val,img = cam.read()
    #img = imutils.resize(img, width=400)
    if img is not None:
        (height,width) = img.shape[:2]
        img = cv.flip(img,1)
        
        #Detect markers
        img, marker_details = detect_markers_in_image(img,
                                                      draw_center = True,
                                                      draw_reference_corner = True,
                                                      target_id = None,
                                                      draw_target_id=True,
                                                      draw_border=True)
        #Print marker details
        if len(marker_details) <= 0:
            send("rc 0 0 0 0")
        elif len(marker_details) > 0:
            center_x,center_y = marker_details[0][0]
            img, x_distance, y_distance, distance = detect_distance_from_image_center(img,
                                                                                        center_x,
                                                                                        center_y)
            
            l_r_speed = int(max_speed * x_distance / width*-1)
            u_d_speed = int(max_speed * y_distance / height*-1)

            print("rc "+str(l_r_speed)+" 0 "+str(u_d_speed)+" 0")
            if distance > min_distance:
                send("rc "+str(l_r_speed)+" 0 "+str(u_d_speed)+" 0")
        #Image display
        cv.imshow('Original webcam image',img)

        #Check for key presses
        pressedKey = cv.waitKey(1)
        if pressedKey == 27:
            send("land")
            break
        elif pressedKey == 107:
            send("emergency")
            break

    
# Close the UDP socket
sock.close()

