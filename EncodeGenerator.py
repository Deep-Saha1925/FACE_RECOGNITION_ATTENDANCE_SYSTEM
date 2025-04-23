import cv2
import face_recognition
import pickle
import os

# Firebase configuration
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Cloudinary configuration
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

cloudinary.config( 
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET,
    secure=True
)

# Import the stdent images from the folder in to list
folderPath = 'Images'
pathList = os.listdir(folderPath)
imageList = []
studentIds = []
print(pathList)

cloudinary_folder = "Images"

for path in pathList:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    
    fileName = f'{folderPath}/{path}'
    
    # Upload image to cloudinary
    public_id = os.path.splitext(path)[0]
    upload_result = cloudinary.uploader.upload(fileName, folder=cloudinary_folder, public_id=public_id)
    print(upload_result["secure_url"])
    
print(len(imageList))

def findEncodings(imagesList):
    encodeList = []
    for image in imagesList:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding started")
encodeListKnown = findEncodings(imageList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding completed")

file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file) #Encodings saved to the pickle file.
file.close()
print("Encode file saved")