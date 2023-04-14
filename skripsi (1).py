import cv2
import numpy as np
import time
import pandas as pd
cam = cv2.VideoCapture(0)
awalan = time.time()
while True:
    ret,frame = cam.read()
    if not ret:
        break
    # lcdDisplay.set('Tekan Tombol t',1)
    # lcdDisplay.set('Untuk Memproses',2)
    frame = cv2.resize(frame,(300,300),interpolation=cv2.INTER_CUBIC)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow('HSV', hsvImage)

    hsv_lower = np.array([12, 52, 0], np.uint8)
    hsv_upper = np.array([73, 255, 255], np.uint8)
    hsv_mask = cv2.inRange(hsvImage, hsv_lower, hsv_upper) 
    #cv2.imshow('masking', hsv_mask)
    cv2.imshow('gambar normal',frame)
    cv2.imshow('gambar hsv', hsvImage)
    kernal = np.ones((5, 5), "uint8")
    
    # morfologi dilasi
    hsv_mask2 = cv2.dilate(hsv_mask, kernal)
    res_hsv = cv2.bitwise_and(hsvImage, hsvImage, 
                                mask = hsv_mask2)
    
    res_normal = cv2.bitwise_and(frame, frame, 
                                mask = hsv_mask)
    
    contours, hierarchy = cv2.findContours(hsv_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('masking normal',res_normal)
    cv2.imshow('masking hsv',res_hsv)
    awalan = time.time()
    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 3000):
                k=cv2.waitKey(1)          
                #kondisi jika t ditekan maka akan menghancurkan semua windows            
                if k%256 == ord('t'):
                        h,s,v = cv2.split(res_hsv)
                        df= pd.DataFrame(h)
                        df = df.replace(0, np.NaN)
                        meanh = np.mean(h)
                        if(meanh < 12):
                            print('daun busuk')
                        else :
                            print('daun sehat')
                        terakhir = time.time()  
                        print ("print",meanh)
                        print ("Total Waktu Komputasi " + str(terakhir- awalan) + " Detik.")
                        cv2.waitKey(0)
                #kondisi jika q ditekan maka akan menghancurkan semua windows            
                elif k%256 == ord('q') :
                        cam.release()
                        cv2.destroyAllWindows()