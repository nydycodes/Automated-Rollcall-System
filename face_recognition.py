import dlib
import cv2
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
from twilio.rest import Client
from datetime import datetime

# enter your respective tokens, sid, and phone number
account_sid = ''
auth_token = ''
twilio_phone_number = ''

known_face_encodings = []
known_face_ids = []

# create a file called known faces within the same directory that stores all the student faces 
known_faces_dir = "known_faces"
for filename in os.listdir(known_faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(known_faces_dir, filename)
        image = dlib.load_rgb_image(image_path)
        face_detector = dlib.get_frontal_face_detector()
        shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

        dets = face_detector(image, 1)
        for k, d in enumerate(dets):
            shape = shape_predictor(image, d)
            face_descriptor = face_rec_model.compute_face_descriptor(image, shape)
            known_face_encodings.append(np.array(face_descriptor))
            known_face_ids.append(os.path.splitext(filename)[0])

# after downloading mysql, enter the user, host, and password specific to your application
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='', 
            database='hostel',
            user='',
            password=''
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def retrieve_details_from_database(id, connection):
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM student WHERE reg_no = '{id}'"
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except Error as e:
        print(f"Error retrieving details from MySQL database: {e}")
        return None

def mark_attendance(id, connection):
    try:
        cursor = connection.cursor()
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"INSERT INTO attendance (student_id, time) VALUES ('{id}', '{time_now}')"
        cursor.execute(query)
        connection.commit()
        print(f"Attendance marked for ID {id} at {time_now}")
    except Error as e:
        print(f"Error marking attendance in MySQL database: {e}")

def send_sms(to_phone_number, message):
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to_phone_number
    )

video_capture = cv2.VideoCapture(0)

connection = connect_to_mysql()

detected_flag = False
sms_sent = False

while True:
    if not detected_flag:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_detector = dlib.get_frontal_face_detector()
        shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

        dets = face_detector(rgb_frame, 1)
        face_ids = []
        for k, d in enumerate(dets):
            shape = shape_predictor(rgb_frame, d)
            face_descriptor = face_rec_model.compute_face_descriptor(rgb_frame, shape)
            face_encoding = np.array(face_descriptor)

            distances = np.linalg.norm(np.array(known_face_encodings) - face_encoding, axis=1)
            min_distance = np.argmin(distances)
            if distances[min_distance] < 0.6:
                id = known_face_ids[min_distance]
            else:
                id = "Unknown"

            face_ids.append(id)
            print(f"Detected ID: {id}")

            if connection:
                if id != "Unknown":
                    records = retrieve_details_from_database(id, connection)
                    if records:
                        for record in records:
                            parents_phone_number = record[3]
                            name_ = record[1]
                            current_time = datetime.now()
                            mark_attendance(id, connection)
                            if current_time.hour >= 18 and current_time.minute >= 30:
                                message = f"Your ward, {name_} is late!"
                            elif current_time.hour >= 17 and current_time.minute >= 30:
                                message = f"Your ward, {name_} is on time!"
                            else:
                                message = f"Your ward, {name_} is early!"
                            send_sms(parents_phone_number, message)
                            print("SMS sent.")
                            sms_sent = True
                    else:
                        print("No details found for this ID in the database")
                else:
                    print("Unknown face detected. No action taken.")

            detected_flag = True

    for d, id in zip(dets, face_ids):
        top = d.top() * 4
        right = d.right() * 4
        bottom = d.bottom() * 4
        left = d.left() * 4

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)
        label_height = 20
        cv2.rectangle(frame, (left, bottom - label_height), (right, bottom), (255, 255, 0), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.5
        font_thickness = 1
        cv2.putText(frame, id, (left + 6, bottom - 6), font, font_scale, (255, 255, 255), font_thickness)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()