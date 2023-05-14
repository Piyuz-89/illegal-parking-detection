# IMPORTING LIBRARIES
import cv2
import easyocr
import re
import time
import pandas as pd
import winsound


# INITIALIZING EASYOCR
reader = easyocr.Reader(['en'])

# SETTING FRAME WIDTH FOR VIDEO CAPTURE WINDOW
frame_width = 640
frame_height = 480

# LOADING PRE-TRAINED DATASET ON NUMBER PLATE
cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
min_area = 500
counter = 0

# START VIDEO CAPTURE
cap = cv2.VideoCapture(0)
cap.set(3,frame_width)   
cap.set(4,frame_height)  
cap.set(10,150)           ##Changing brightness to 150

while True:
    success, img = cap.read()

    # CONVERTING RGB IMAGE TO GRAYSCALE
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # """Using pretrained OpenCV number plate cascade"""

    number_plates = cascade.detectMultiScale(img_gray, 1.1, 5)

    """Creating boundary boxes around detected number plates"""
    # CREATING BOUNDARY BOXES AROUND DETECTED NUMBER PLATE

    for (x,y,w,h) in number_plates:
        area = w*h
        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255),2)
            cv2.putText(img, "Number Plate",(x,y-5), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255), 2)
            
            """Picking the number plate from the caption"""
            # SEPARATING NUMBER PLATE FROM REAL TIME VIDEO CAPTURE 

            img_roi = img[y:y+h, x:x+w]
            cv2.imshow("Region of Interest", img_roi)
            
            # USING EASYOCR TO RECOGNIZE TEXT FROM EXTRACTED NUMBER PLATE
            text1 = reader.readtext(img_roi)

            if len(text1) == 0:
                continue
            else:
                # CONVERT THE OCR TEXT TO UPPERCASE
                res2 = str("".join(re.split("[^a-zA-Z0-9]*", text1[0][1]))).upper()
                print("No. Plate: "+res2)

            # READING VALID NUMBER PLATES FROM DATASET
            df = pd.read_csv('Book1.csv')

            # CHECKING IF THE EXTRACTED NUMBER PLATE IS VALID OR NOT 
            isValid = res2 in df['NoPlate'].unique()

            if isValid:
                print("Vehicle is allowed")
               
            else:
                print("Vehicle is not allowed")
                winsound.Beep(440, 5000)      # PLAYS BEEP FOR 5 SECONDS AT 440 Hz FREQUENCY



    time.sleep(5) # TIMER FOR FRAME CAPTURE

    # DISPLAYING VIDEO CAPTURE 
    cv2.imshow("Capture", img)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        break

cap.release()
cv2.destroyAllWindows()
