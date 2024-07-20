# Automated-Rollcall-System

This is an automated roll call system for hostel students utilizing face recognition technology with dlib and OpenCV. 
The system stores student information, including ID, name, address, email, and parent’s contact details, in a MySQL database. 
Real-time SMS notifications are sent via Twilio to inform parents if their ward marks attendance late. 
The system marks attendance, displays the time, and logs it in the database, enhancing hostel management and parent communication by providing timely updates on attendance and punctuality.

Pre-requisites: 
1. Download packages such as dlib(face recognition), openCV(image processing), mysql connector(interacting w/ databases), twilio(send sms)
2. Create account in twillio and authorize your phone numbers
3. Download MySQL server as well as workbench for a friendly IDE
4. Download "shape_predictor_68_face_landmarks.dat" and "dlib_face_recognition_resnet_model_v1.dat" files
