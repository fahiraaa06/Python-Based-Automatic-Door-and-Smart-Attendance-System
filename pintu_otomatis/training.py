# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:27:34 2020

@author: FAHMI-PC
"""

import os
import dlib
from skimage import io
import csv
import numpy as np


path_images_from_camera = "data/create/"

# Dlib detector

detector = dlib.get_frontal_face_detector()

# Dlib predictor

predictor = dlib.shape_predictor("data/data_dlib/shape_predictor_68_face_landmarks.dat")

# Dlib

# sebagai model
face_rec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


#fungsi untuk membuat training

def return_128d_features(path_img):
    img_rd = io.imread(path_img)
    faces = detector(img_rd, 1)


    print("%-40s %-20s" % ("image with faces detected:", path_img), '\n')

    # 因di atas melakukan print jika wajah terdeteksi


    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_rec.compute_face_descriptor(img_rd, shape)
        
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor


# ini file csv
    
def return_features_mean_personX(path_faces_personX):
    features_list_personX = []
    photos_list = os.listdir(path_faces_personX)
    
    if photos_list:
        for i in range(len(photos_list)):
            
            print("%-40s %-20s" % ("image to read:", path_faces_personX + "/" + photos_list[i]))
            features_128d = return_128d_features(path_faces_personX + "/" + photos_list[i])
           
            
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
                
    else:
        print(" Warning: Tidak ada images di " + path_faces_personX + '/', '\n')

   
    # person X
    
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
        
    else:
        features_mean_personX = '0'

    return features_mean_personX


# mendapatkan number of latest person
    
person_list = os.listdir("data/create/")

person_num_list = []

for person in person_list:
    
    person_num_list.append(int(person.split('_')[-1]))
person_cnt = max(person_num_list)

with open("data/features_all.csv", "w", newline="") as csvfile:
    
    writer = csv.writer(csvfile)
    
    for person in range(person_cnt):
        # Get the mean/average features of face/personX, it will be a list with a length of 128D
        
        print(path_images_from_camera + "person_"+str(person+1))
        
        features_mean_personX = return_features_mean_personX(path_images_from_camera + "person_"+str(person+1))
        
        writer.writerow(features_mean_personX)
        
        
        #print menunjukkan jumlah people
        print("People of features:", list(features_mean_personX))
        
        #ini save ke csv
        print('\n')
        
    print("Save all the features of faces registered into: data/features_all.csv")
    
    
    