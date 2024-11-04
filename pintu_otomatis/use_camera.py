# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:27:34 2020

@author: FAHMI-PC
"""

import cv2

cap = cv2.VideoCapture(0)



# ukuran default
# ini adalah untuk cap untuk munculkan frame vidio

# jika cap.isOpened()
print(cap.isOpened())

# cap.read()

""" 

ini adalah
kondisi dimana face terdeteksi

"""

while cap.isOpened():
    ret_flag, img_camera = cap.read()

    print("height: ", img_camera.shape[0])
    print("width:  ", img_camera.shape[1])
    print('\n')

    cv2.imshow("camera", img_camera)

    # variabel k wait 
    k = cv2.waitKey(1)

    # tekan s
    if k == ord('s'):
        cv2.imwrite("test.jpg", img_camera)

    # tekan q
    if k == ord('q'):
        break

# munculkan frame
cap.release()

# exit all
cv2.destroyAllWindows()
