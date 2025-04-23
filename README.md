# Face Recognition Attendance System

A real-time **Face Recognition Attendance System** that uses **AI & ML** to recognize faces and mark attendance. This project integrates with **Firebase** for database management and **Cloudinary** for image storage.

---

## Features

- **Real-Time Face Recognition**: Detect and recognize faces using a webcam.
- **Attendance Management**: Automatically updates attendance records in Firebase.
- **Cloud Integration**:
  - **Firebase**: Stores student data and attendance records.
  - **Cloudinary**: Stores student images securely in the cloud.
- **AI-Powered Encoding**: Uses `face_recognition` library to encode and compare faces.
- **Interactive UI**: Displays real-time attendance updates with a visually appealing interface.

---

## Project Structure


FACE_RECOGNITION_PROJECT/ ├── AddDataToDB.py # Script to add student data to Firebase ├── EncodeGenerator.py # Generates face encodings and uploads images to Cloudinary ├── Main.py # Main application for real-time face recognition ├── config.py # Configuration file for environment variables ├── .env # Environment variables (Cloudinary & Firebase credentials) ├── Images/ # Folder containing student images ├── Resources/ # UI resources (background and mode images) ├── EncodeFile.p # Pickle file storing face encodings ├── README.md # Project documentation


---

## Prerequisites

1. **Python 3.10+**
2. Install required libraries:
   ```bash
   pip install -r requirements.txt