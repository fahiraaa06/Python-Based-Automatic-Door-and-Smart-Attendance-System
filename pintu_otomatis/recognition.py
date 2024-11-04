
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:23:05 2020

@author: FAHMI-PC
"""

import dlib          
import numpy as np  
import cv2           
import pandas as pd  
import os
import multiprocessing as jalan
from threading import Thread


# face recognition model, untuk deteksi wajah

# ini adalah model yang digunakan
facerec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


# fungsi ini sebagai between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist

# fungsi start pada thread
def start(self):
        Thread(target=self.update, args=()).start()
        return self


# melakukan cek csv
if os.path.exists("data/features_all.csv"):
    path_features_known_csv = "data/features_all.csv"
    csv_rd = pd.read_csv(path_features_known_csv, header=None)

    # setelah itu 
    # array akan di save
    features_known_arr = []

    # melakukan print known faces
    
    for i in range(csv_rd.shape[0]):
        features_someone_arr = []
        for j in range(0, len(csv_rd.iloc[i])):
            features_someone_arr.append(csv_rd.iloc[i][j])
        features_known_arr.append(features_someone_arr)
    print("Faces in Database：", len(features_known_arr))

    # Dlib detejsu
    # detector dan predictor yang digunakan
    detector = dlib.get_frontal_face_detector()
    
    predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

    # munculkan webcam
    cap = cv2.VideoCapture(0)

    # jika webcam terbuka 
    
    while cap.isOpened():

        #sebagai flag sebelumnya untuk read wajah
        flag, img_rd = cap.read()
        
        faces = detector(img_rd, 0)

        # font untuk di tulis 
        font = cv2.FONT_ITALIC

        # list to save the posisi dan nama
        pos_namelist = []
        name_namelist = []

        kk = cv2.waitKey(1)

        # untuk menunggu 
        # tekan 'q' untuk exit
        if kk == ord('q'):
            break
        else:
            # jika wajah terdeteksi
            if len(faces) != 0:
                # features_cap_arr
                # capture dan save into features_cap_arr
                
                features_cap_arr = []
                for i in range(len(faces)):
                    shape = predictor(img_rd, faces[i])
                    features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))


                # convert to the database csv
                for k in range(len(faces)):
                    print("##### camera person", k+1, "#####")
                    # 
                    # jika ada yang unknown
                    # Set the default names of faces with "unknown"
                    name_namelist.append("unknown")

                    # posisi di capture
                    pos_namelist.append(tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top())/4)]))

                    # face sudah di database
                    
                    e_distance_list = []
                    
                    for i in range(len(features_known_arr)):
                
                        if str(features_known_arr[i][0]) != '0.0':
                            print("with person", str(i + 1), "the e distance: ", end='')
                            e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                            print(e_distance_tmp)
                            e_distance_list.append(e_distance_tmp)
                        
                        else:
                          
                            e_distance_list.append(999999999)
                            
                    # temukan minimal 1 person
                    similar_person_num = e_distance_list.index(min(e_distance_list))
                    print("Minimum e distance with person", int(similar_person_num)+1)

                    if min(e_distance_list) < 0.4:
                       
                        # person1, 2, 3 .....
                        
                        name_namelist[k] = "Person "+str(int(similar_person_num)+1)
                        print("May be person "+str(int(similar_person_num)+1))
                    else:
                        print("Unknown person")

                    # ini sudah membaca person
                    
                 
                    for kk, d in enumerate(faces):
                        
                        cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                    print('\n')


                # menulis nama under rectangle
                for i in range(len(faces)):
                    cv2.putText(img_rd, name_namelist[i], pos_namelist[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

        print("Faces in camera now:", name_namelist, "\n")

        cv2.putText(img_rd, "Press 'q': Quit", (20, 450), font, 0.8, (84, 255, 159), 1, cv2.LINE_AA)
        
        cv2.putText(img_rd, "Face Recognition", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        
        cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow("camera", img_rd)

    cap.release()
    
    cv2.destroyAllWindows()


#fungsi pool dari multiprocessing
    
if __name__ == "__main__":
    pool = jalan.Pool(jalan.cpu_count()- 1)
    cap.release()
    cv2.destroyAllWindows()


else:
    print('##### Warning #####', '\n')
    print("'features_all.py' not found!")
    print("Please run 'get_faces_from_camera.py' and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'", '\n')
    print('##### Warning #####')