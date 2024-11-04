
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:05:11 2020

@author: FAHMI-PC
"""

#import library

import os
import sys
import cv2
import csv
import easygui


import smtplib
import mimetypes
import datetime
import numpy as np
import pandas as pd
import time

from threading import Thread
import multiprocessing as jalan

from skimage import io
from email import encoders
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfilename
from email.mime.multipart import MIMEMultipart

import dlib                           
import shutil

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = mainScreen (root)
    root.mainloop()

w = None
def create_mainScreen(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = mainScreen (w)
    AMS_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_mainScreen():
    global w
    w.destroy()
    w = None

class mainScreen:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {SF Pro Display} -size 14 -weight bold -slant"  \
            " roman -underline 0 -overstrike 0"
        font10 = "-family {SF Pro Display} -size 14 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font11 = "-family {SF Pro Display} -size 14 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        font12 = "-family {SF Pro Display} -size 12 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"

#Take image
        def takeImage():
        	detector_face = dlib.get_frontal_face_detector()
        	cap_face = cv2.VideoCapture(0)
        	cnt_ss_face = 0
        	current_face_dir = ""
        	path_photos_from_camera = "data/create/"

        	def ambyar_work_mkdir():
        		if os.path.isdir(path_photos_from_camera):
        			pass
        		else:
        			os.mkdir(path_photos_from_camera)
        	ambyar_work_mkdir()


        	def ambyar_work_del_old_face_folders():
        		folders_rd = os.listdir(path_photos_from_camera)
        		for i in range(len(folders_rd)):
        			shutil.rmtree(path_photos_from_camera+folders_rd[i])
        		if os.path.isfile("data/features_all.csv"):
        			os.remove("data/features_all.csv")

        	if os.listdir("data/create/"):
        		person_list = os.listdir("data/create/")
        		person_num_list = []
        		for person in person_list:
        			person_num_list.append(int(person.split('_')[-1]))
        		person_cnt = max(person_num_list)

        	else:
        		person_cnt = 0
        	save_flag = 1
        	press_n_flag = 0

        	while cap_face.isOpened():
        		flag, img_rd = cap_face.read()
        		kk_ambyar = cv2.waitKey(1)
        		faces = detector_face(img_rd, 0)
        		font = cv2.FONT_ITALIC

        		if kk_ambyar == ord('n'):
        			person_cnt += 1
        			current_face_dir = path_photos_from_camera + "person_" + str(person_cnt)
        			os.makedirs(current_face_dir)
        			print('\n')
        			print(" Buat Folder: ", current_face_dir)
        			cnt_ss = 0
       				press_n_flag = 1

        		if len(faces) != 0:
        			for k, d in enumerate(faces):
        				pos_start = tuple([d.left(), d.top()])
        				pos_end = tuple([d.right(), d.bottom()])
        				height = (d.bottom() - d.top())
        				width = (d.right() - d.left())
        				hh = int(height/2)
        				ww = int(width/2)
        				color_rectangle = (255, 255, 255)

        				if (d.right()+ww) > 640 or (d.bottom()+hh > 480) or (d.left()-ww < 0) or (d.top()-hh < 0):
        					cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        					color_rectangle = (0, 0, 255)
        					save_flag = 0
        					if kk_ambyar == ord('s'):
        						print(" Tolong sesuaikan di posisi")
        				else:
        					color_rectangle = (255, 255, 255)
        					save_flag = 1

        				cv2.rectangle(img_rd,tuple([d.left() - ww, d.top() - hh]),
        					tuple([d.right() + ww, d.bottom() + hh]),color_rectangle, 2)
        				img_blank = np.zeros((int(height*2), width*2, 3), np.uint8)

        				if save_flag:
        					if kk_ambyar == ord('s'):
        						if press_n_flag:
        							cnt_ss += 1
        							for ii in range(height*2):
        								for jj in range(width*2):
        									img_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
        							cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", img_blank)
        							print(" Save into：", str(current_face_dir) + "/img_face_" + str(cnt_ss) + ".jpg")
        						else:
        							print(" Tolong Jika 'N' Sebelum 'S'")

        		cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        		cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        		cv2.putText(img_rd, "N: Create face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
        		cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
        		cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

        		if kk_ambyar == ord('q'):
        			break

        		cv2.imshow("camera", img_rd)

        	cap_face.release()
        	cv2.destroyAllWindows()

#training data image
        def trainImage():
            path_images_from_camera = "data/create/"
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor("data/data_dlib/shape_predictor_68_face_landmarks.dat")
            face_rec = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

            def return_128d_features(path_img):
                img_rd = io.imread(path_img)
                faces = detector(img_rd, 1)


                print("%-40s %-20s" % ("image with faces detected:", path_img), '\n')

    

                if len(faces) != 0:
                    shape = predictor(img_rd, faces[0])
                    face_descriptor = face_rec.compute_face_descriptor(img_rd, shape)
        
                else:
                    face_descriptor = 0
                    print("no face")

                return face_descriptor


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

  
                if features_list_personX:
                    features_mean_personX = np.array(features_list_personX).mean(axis=0)
        
                else:
                    features_mean_personX = '0'

                return features_mean_personX


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
        
                    print("People of features:", list(features_mean_personX))
        
                    print('\n')
        
                print("Save all the features of faces registered into: data/features_all.csv")
    
    
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            IDS = []
            for imagePath in imagePaths:
                pilImage = Image.open(imagePath).convert('L')
                imageNp = np.array(pilImage, 'uint8')
                Id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(imageNp)
                for (x, y, w, h) in faces:
                    faceSamples.append(imageNp[y:y + h, x:x + w])
                    IDS.append(Id)
            return faceSamples, IDS

#buka pintu recognition
        def bukaPintu():
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
                                print("PINTU TERBUKA", k+1, "#####")
                                # 
                                # jika ada yang unknown
                                # Set the default names of faces with "unknown"
                                name_namelist.append("PINTU TIDAK TERBUKA")

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
                        
                                    name_namelist[k] = "PINTU TERBUKA, PERSON "+str(int(similar_person_num)+1)
                                    easygui.msgbox("Pintu Terbuka", title="Buka Pintu")
                                    print("May be person "+str(int(similar_person_num)+1))

                                else:
                                    print("PINTU TIDAK TERBUKA")

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


#tutup pintu
        def tutupPintu():
            easygui.msgbox("Pintu Ditutup", title="Tutup Pintu")


        
        top.geometry("1367x696+-9+0")
        top.minsize(120, 1)
        top.maxsize(1370, 749)
        top.resizable(0, 0)
        top.iconbitmap("icon.ico")
        top.focus_force()
        top.title("PINTU OTOMATIS - FACE 2 UNLOCK")
        top.configure(background="#1B1B1B")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Title = tk.Message(top)
        self.Title.place(relx=-0.007, rely=0.042, relheight=0.134, relwidth=1.005)
        self.Title.configure(background="#00008B")
        self.Title.configure(font="-family {SF Pro Display} -size 36 -weight bold")
        self.Title.configure(foreground="#FFFFFF")
        self.Title.configure(highlightbackground="#D9D9D9")
        self.Title.configure(highlightcolor="black")
        self.Title.configure(text='''PINTU OTOMATIS - FACE 2 UNLOCK''')
        self.Title.configure(width=1374)

        self.Details = tk.Message(top)
        self.Details.place(relx=0.070, rely=0.200, relheight=0.350, relwidth=0.600)
        self.Details.configure(background="#FF4D00")
        self.Details.configure(font=font12)
        self.Details.configure(foreground="#ffffff")
        self.Details.configure(highlightbackground="#d9d9d9")
        self.Details.configure(highlightcolor="black")
        self.Details.configure(text='''PINTU OTOMATIS BERBASIS FACE RECOGNITION

Demo : Keadaan pintu tertutup, seseorang ingin masuk maka kita klik button BUKA PINTU.
lalu seseorang memperlihatkan wajar nya ke kamera, secara otomatis jika 
wajah terdeteksi maka pintu terbuka dengan hal ini ada notifikasi PINTU TERBUKA !
Jika wajah tidak terdeteksi maka tidak ada notifikasi pintu terbuka dan akan ada 
notifikasi pintu tidak terbuka. Jika kita ingin menutup pintu maka klik button TUTUP PINTU.''') 
        self.Details.configure(width=1000)

        self.Notification = tk.Label(top)
        self.Notification.configure(text="DEMO PROGRAM PINTU OTOMATIS DENGAN FACE RECOGNITION")
        self.Notification.configure(background="#FF4D00")
        self.Notification.configure(foreground="#FFFFFF")
        self.Notification.configure(width=64, height=2)
        self.Notification.configure(font="-family {SF Pro Display} -size 16 -weight bold")
        self.Notification.place(x=92, y=430)

        self.takeImages = tk.Button(top)
        self.takeImages.place(relx=0.067, rely=0.818, height=38, width=133)
        self.takeImages.configure(activebackground="#ececec")
        self.takeImages.configure(activeforeground="#000000")
        self.takeImages.configure(background="#2E2E2E")
        self.takeImages.configure(disabledforeground="#a3a3a3")
        self.takeImages.configure(font=font10)
        self.takeImages.configure(foreground="#FFFFFF")
        self.takeImages.configure(highlightbackground="#d9d9d9")
        self.takeImages.configure(highlightcolor="black")
        self.takeImages.configure(pady="0")
        self.takeImages.configure(text='''Take Images''')
        self.takeImages.configure(command=takeImage)

        self.trainStudent = tk.Button(top)
        self.trainStudent.place(relx=0.205, rely=0.818, height=38, width=139)
        self.trainStudent.configure(activebackground="#ececec")
        self.trainStudent.configure(activeforeground="#000000")
        self.trainStudent.configure(background="#2E2E2E")
        self.trainStudent.configure(disabledforeground="#a3a3a3")
        self.trainStudent.configure(font=font11)
        self.trainStudent.configure(foreground="#FFFFFF")
        self.trainStudent.configure(highlightbackground="#d9d9d9")
        self.trainStudent.configure(highlightcolor="black")
        self.trainStudent.configure(pady="0")
        self.trainStudent.configure(text='''Training Data''')
        self.trainStudent.configure(command=trainImage)

        self.automaticAttendance = tk.Button(top)
        self.automaticAttendance.place(relx=0.344, rely=0.818, height=38, width=220)
        self.automaticAttendance.configure(activebackground="#ececec")
        self.automaticAttendance.configure(activeforeground="#000000")
        self.automaticAttendance.configure(background="#2E2E2E")
        self.automaticAttendance.configure(disabledforeground="#a3a3a3")
        self.automaticAttendance.configure(font=font11)
        self.automaticAttendance.configure(foreground="#FFFFFF")
        self.automaticAttendance.configure(highlightbackground="#d9d9d9")
        self.automaticAttendance.configure(highlightcolor="black")
        self.automaticAttendance.configure(pady="0")
        self.automaticAttendance.configure(text='''Buka Pintu''')
        self.automaticAttendance.configure(command=bukaPintu)

        self.manualAttendance = tk.Button(top)
        self.manualAttendance.place(relx=0.541, rely=0.818, height=38, width=194)
        self.manualAttendance.configure(activebackground="#ececec")
        self.manualAttendance.configure(activeforeground="#000000")
        self.manualAttendance.configure(background="#2E2E2E")
        self.manualAttendance.configure(disabledforeground="#a3a3a3")
        self.manualAttendance.configure(font=font11)
        self.manualAttendance.configure(foreground="#FFFFFF")
        self.manualAttendance.configure(highlightbackground="#d9d9d9")
        self.manualAttendance.configure(highlightcolor="black")
        self.manualAttendance.configure(pady="0")
        self.manualAttendance.configure(text='''Tutup Pintu''')
        self.manualAttendance.configure(command=tutupPintu)

        self.authorDetails = tk.Message(top)
        self.authorDetails.place(relx=0.753, rely=0.46, relheight=0.407, relwidth=0.19)
        self.authorDetails.configure(background="#2E2E2E")
        self.authorDetails.configure(font=font12)
        self.authorDetails.configure(foreground="#ffffff")
        self.authorDetails.configure(highlightbackground="#d9d9d9")
        self.authorDetails.configure(highlightcolor="black")
        self.authorDetails.configure(text='''FACE 2 UNLOCK -            
TUGAS BESAR SISTEM PAKAR

1. Muhammad Fahmi - 1174021
2. M Dzihan Al-Banna - 1174095
3. M Tomy Nur Maulidy - 1174031
4. Choirul Anam - 1174004
5. Damara Benedikta S - 1174012
6. Dezha Aidil Martha - 1174025''') 
        self.authorDetails.configure(width=260)


# Disini mulai reload module dari do_something
if __name__ == '__main__':
    vp_start_gui()