import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyzbar.pyzbar import decode

input_dir = r"C:\Users\user\OneDrive\Documents\Computer Vision\Beginner_projects\QR_reader+attendance_system\QR_codes\pngtree-scan-me-qrcode-design-png-png-image_6531526.jpg"
img = cv2.imread(os.path.join(input_dir))

qr_info = decode(img)
# print(len(qr_info))

for qr in qr_info:
    data = qr.data
    rect = qr.rect
    polygon = qr.polygon

    print(data)
    print(rect)
    print(polygon)

    # Draw the rectangle
    img = cv2.rectangle(img,
        (rect.left, rect.top), 
        (rect.left + rect.width, rect.top + rect.height), 
        (0, 255, 0), 
        5)

    # Draw the polygon
    img = cv2.polylines(img, [np.array(polygon)], True, (0, 0, 255), 5)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()