import cv2 as cv
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image
# Set up video capture from webcam
cam = cv.VideoCapture(0)

while True:
    #Read a camera frame
    ret_val,img = cam.read()
    img = cv.flip(img,1)
    img = imutils.resize(img, width=400)

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
    #Image display
    cv.imshow('Original webcam image',img)

    #Check for key presses
    pressedKey = cv.waitKey(100)
    if pressedKey == 27:
        break
    

