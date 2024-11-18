from data_formation_icus import fetch_icu_data
from data_formation_attendance import fetch_attendance_data
import firebase_admin
from firebase_admin import credentials, db


def final_formation():
    
    cred = credentials.Certificate('Backend_majorproject/hand_wash_json_file.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://handhygiene-jaypeehealthcare-default-rtdb.firebaseio.com/'
    })
    
    fetch_icu_data()
    name = fetch_attendance_data()
    return name
    

print(final_formation())