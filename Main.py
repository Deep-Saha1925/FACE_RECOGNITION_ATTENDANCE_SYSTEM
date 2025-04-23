import cv2
import os
import pickle
import face_recognition
import cvzone
import requests
import numpy as np
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import threading

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CREDENTIAL_PATH

cloudinary.config( 
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET,
    secure=True
)

# database configuration
cred = credentials.Certificate(CREDENTIAL_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancerealtime-dff5d-default-rtdb.firebaseio.com/'
})

# Video capture from webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Import the images from the folder in to list
forlderModePath = 'Resources/Modes'
imgModeLists = []
for path in os.listdir(forlderModePath):
    imgModeLists.append(cv2.imread(os.path.join(forlderModePath, path)))

# Load the encoding file
print("Loading encoded file..")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds

modeType = 0
counter = 0
id = -1
imageStudent = []


# Function to download the image from cloudinary
def download_image(student_id):
    global imageStudent
    url = f'https://res.cloudinary.com/dvqpheh0p/image/upload/Images/{student_id}'
    response = requests.get(url)
    array = np.frombuffer(response.content, np.uint8)
    imageStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
    return imageStudent

while True:
    success, img = cap.read()
    
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)
    
    faceCurrFrame = face_recognition.face_locations(imgSmall)
    encodeCurrFrame = face_recognition.face_encodings(imgSmall, faceCurrFrame)
    
    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeLists[modeType]
    
    if faceCurrFrame:

        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIdx = np.argmin(faceDis)
            if matches[matchIdx]:
                # print("Known student found")
                # print(studentIds[matchIdx])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, 20, rt=0)
                id = studentIds[matchIdx]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading..", (275, 400), scale=3, thickness=3, colorR=(0, 0, 0))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the data
                studentInfo = db.reference(f'Students/{id}').get()
                
                #Get image from cloudinary
                download_thread = threading.Thread(target=download_image, args=(id,))
                download_thread.start()
                
                # Update the attendance for the student
                dateTimeObj = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - dateTimeObj).total_seconds()
                
                if secondsElapsed > 80: #Time interval to update attendance
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633, 808:808+414] = imgModeLists[modeType]
                    cv2.putText(imgBackground, str(studentInfo['name']), (905, 281), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    
            if modeType != 3:
                
                if 60 < counter < 80:
                    modeType = 2
                    
                imgBackground[44:44+633, 808:808+414] = imgModeLists[modeType]
                    
                if counter <= 60:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(imgBackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 2)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 2)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 2)
                
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 2)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 2)
                
                    imgBackground[175:175 + 216, 909:909 + 216] = imageStudent
            
                counter += 1
                
                if counter >= 80:
                    # Reset All values
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imageStudent = []
                    imgBackground[44:44+633, 808:808+414] = imgModeLists[modeType]
                
    else:
        modeType = 0
        counter = 0
        imgBackground[44:44+633, 808:808+414] = imgModeLists[modeType]
        
    cv2.imshow("Web Cam", img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()