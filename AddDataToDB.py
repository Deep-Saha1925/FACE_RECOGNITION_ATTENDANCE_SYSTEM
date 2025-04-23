import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from config import CREDENTIAL_PATH

cred = credentials.Certificate(CREDENTIAL_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancerealtime-dff5d-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')
data = {
    "236598": {
        "name": "Netaji",
        "major": "Economics",
        "starting_year": 1920,
        "total_attendance": 10,
        "standing": "O",
        "year": 4,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "258036": {
        "name": "Virat Kohli",
        "major": "Cricket",
        "starting_year": 2004,
        "total_attendance": 18,
        "standing": "A",
        "year": 4,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "357951": {
        "name": "Dhoni",
        "major": "TT",
        "starting_year": 2002,
        "total_attendance": 7,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "365412": {
        "name": "Sachin",
        "major": "Cricket",
        "starting_year": 1990,
        "total_attendance": 10,
        "standing": "O",
        "year": 2,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "3698741": {
        "name": "Bumrah",
        "major": "Bowler",
        "starting_year": 2018,
        "total_attendance": 8,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "321654": {
        "name": "Deep Saha",
        "major": "CSE",
        "starting_year": 2022,
        "total_attendance": 7,
        "standing": "G",
        "year": 3,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "852741": {
        "name": "Emilie Blunt",
        "major": "Economics",
        "starting_year": 2023,
        "total_attendance": 2,
        "standing": "B",
        "year": 2,
        "last_attendance_time": "2025-03-31 00:54:34",
    },
    "963852": {
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 15,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2025-03-31 00:54:34",
    }
}

for key, value in data.items():
    ref.child(key).set(value)