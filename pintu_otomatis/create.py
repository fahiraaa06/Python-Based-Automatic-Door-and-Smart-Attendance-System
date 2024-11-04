# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:27:34 2020

@author: FAHMI-PC
"""


#ini kodingan untuk membuat dataset

import dlib         
import numpy as np  
import cv2          
import os           
import shutil

# load detector

detector_face = dlib.get_frontal_face_detector()

# load camera

cap_face = cv2.VideoCapture(0)

# melakukan capture wajah

cnt_ss_face = 0

# membuat folder untuk simpan wajah

current_face_dir = ""

# ini tempat penyimpanan

path_photos_from_camera = "data/create/"


# membuat fungsi

# tempat penyimpanan foto atau wajah

def ambyar_work_mkdir():

    # membuat lokasi
    if os.path.isdir(path_photos_from_camera):
        pass
    else:
        os.mkdir(path_photos_from_camera)


ambyar_work_mkdir()


##### ------ #####

# membuat fungsi selanjutnya
# menghapus data yang lama

def ambyar_work_del_old_face_folders():

    # save data to "/data_faces_from_camera/person_x/"...
    folders_rd = os.listdir(path_photos_from_camera)
    for i in range(len(folders_rd)):
        shutil.rmtree(path_photos_from_camera+folders_rd[i])
        
    #disini kita membuat file csv nya
    if os.path.isfile("data/features_all.csv"):
        os.remove("data/features_all.csv")


# akan menghapus file yang lama jika ada
# dengan fungsi di atas
        
##################################


# melakukan cek terhadap people

# mulai dari person_1
        
if os.listdir("data/create/"):
    # mendapatkan latest person
    person_list = os.listdir("data/crate/")
    person_num_list = []
    for person in person_list:
        person_num_list.append(int(person.split('_')[-1]))
    person_cnt = max(person_num_list)

# cek ke person 1
# person_1
    
else:
    person_cnt = 0

# flag untuk melakukan save
save_flag = 1

# jika n di tekan 
press_n_flag = 0


while cap_face.isOpened():
    flag, img_rd = cap_face.read()
    # ini memprint fungsi (img_rd.shape)
    # ukuran secara default
    # 1280x720

    kk_ambyar = cv2.waitKey(1)

    # load detector
    faces = detector_face(img_rd, 0)

    # font untuk menulis nya
    font = cv2.FONT_ITALIC

    # tekan 'n' untuk create the folders untuk wajah
    
    if kk_ambyar == ord('n'):
        person_cnt += 1
        current_face_dir = path_photos_from_camera + "person_" + str(person_cnt)
        os.makedirs(current_face_dir)
        
        print('\n')
        
        print(" Buat Folder: ", current_face_dir)

        #clear 
        
        cnt_ss = 0
        
        press_n_flag = 1
        

    #ini jika face terdeteksi
    
    if len(faces) != 0:
        # show di dalam box yang telah dibuat
        for k, d in enumerate(faces):
           
            # (x,y), sebagai panjang x lebar
            pos_start = tuple([d.left(), d.top()])
            
            pos_end = tuple([d.right(), d.bottom()])

            # lebih detail nya seperti ini
            height = (d.bottom() - d.top())
            
            width = (d.right() - d.left())

            hh = int(height/2)
            
            ww = int(width/2)

            # warna jika face terdeteksi
            color_rectangle = (255, 255, 255)

            # ukuran nya 480x640
            if (d.right()+ww) > 640 or (d.bottom()+hh > 480) or (d.left()-ww < 0) or (d.top()-hh < 0):
                cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                color_rectangle = (0, 0, 255)
                save_flag = 0
                
                if kk_ambyar == ord('s'):
                    print(" Tolong sesuaikan di posisi")
            else:
                color_rectangle = (255, 255, 255)
                save_flag = 1
            
            #ini ukuran nya
            cv2.rectangle(img_rd,
                          tuple([d.left() - ww, d.top() - hh]),
                          tuple([d.right() + ww, d.bottom() + hh]),
                          color_rectangle, 2)

            # membuat blank image
            img_blank = np.zeros((int(height*2), width*2, 3), np.uint8)

            if save_flag:
                # tekan's' jika save wajah
                if kk_ambyar == ord('s'):
                    # cek jika tekan 'n'
                    if press_n_flag:
                        cnt_ss += 1
                        for ii in range(height*2):
                            for jj in range(width*2):
                                img_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
                        cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", img_blank)
                        print(" Save into：", str(current_face_dir) + "/img_face_" + str(cnt_ss) + ".jpg")
                    else:
                        print(" Tolong Jika 'N' Sebelum 'S'")

    # melihat face nya berapa yang sudah ada
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    # melakukan tekan  keyboard
    cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    
    cv2.putText(img_rd, "N: Create face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    
    cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    
    cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

    # untuk exit
    if kk_ambyar == ord('q'):
        break



    cv2.imshow("camera", img_rd)

# release camera 
cap_face.release()
cv2.destroyAllWindows()


