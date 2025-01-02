import os
import cv2
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode  # Ensure you have pyzbar installed

# Read the authorized users from the whitelist file
with open(r'./whitelist.txt', 'r') as file:
    authorized_users = [line.strip() for line in file.readlines() if len(line.strip()) > 0]

log_path = r'./attendance.txt'

cap = cv2.VideoCapture(0)

most_recent_access = {}
time_between_logs = 5

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        break

    qr_info = decode(frame)

    if len(qr_info) > 0:
        qr = qr_info[0]
        data = qr.data.decode('utf-8')  # Decode the data to a string
        rect = qr.rect
        polygon = qr.polygon

        if data in authorized_users:
            cv2.putText(frame, 'Authorized', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
            if data not in most_recent_access or time.time() - most_recent_access[data] > time_between_logs:
                most_recent_access[data] = time.time()
                with open(log_path, 'a') as log_file:
                    log_file.write('{}, {}\n'.format(data, datetime.datetime.now()))
        else:
            cv2.putText(frame, 'Unauthorized', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

        # Draw the rectangle
        frame = cv2.rectangle(frame,
            (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
            (0, 255, 0),
            3)

        # Draw the polygon
        frame = cv2.polylines(frame, [np.array(polygon)], True, (0, 0, 255), 3)

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# if len(qr_info) > 0:
#     qr = qr_info[0]
#     data = qr.data
#     rect = qr.rect
#     polygon = qr.polygon

#     # if data.decode('utf-8') in authorized_users:
#     cv2.putText(frame, data.decode(), (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
#     # else:
#         # cv2.putText(frame, 'Unauthorized', (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

#     # Draw the rectangle
#     frame = cv2.rectangle(frame,
#         (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
#         (0, 255, 0),
#         5)

#     # Draw the polygon
#     frame = cv2.polylines(frame, [np.array(polygon)], True, (0, 0, 255), 5)