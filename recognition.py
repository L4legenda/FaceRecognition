import face_recognition
import numpy as np
import requests
from datetime import date, datetime
from parseUsers import parseUsers

known_face_encodings = []
known_face_names = []


for user in parseUsers():
    user_image = face_recognition.load_image_file("./image/" + user["Photo"])
    user_face_encoding = face_recognition.face_encodings(user_image)[0]

    known_face_encodings.append(user_face_encoding)
    known_face_names.append(user["Login"])


process_this_frame = True
face_locations = []
face_encodings = []
face_names = []



def rec(image):
    global face_locations
    global face_encodings
    global face_names
    global process_this_frame

    frame = image

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                now = datetime.now()

                r = requests.post("http://23.105.226.115/api/user/lesson", json={
                    "User": known_face_names[best_match_index],
                    "FullDate": now.strftime("%Y-%m-%d"),
                    "Presence": True
                })
                print(r.text)

            face_names.append(name)
        print(face_names)

    process_this_frame = not process_this_frame


    

    # Display the resulting image
    return {
        "face_locations" : face_locations,
        "face_names" : face_names
    }