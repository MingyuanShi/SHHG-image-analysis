# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 10:44:30 2019
ver 1.0
@author: myshi
"""
import cv2 as cv
import numpy as np 
from matplotlib import pyplot as plt
import math
import xlwt
import os

##################################################

def CONTOURS(image):
    
    image_blur =cv.GaussianBlur(image, (5,5), 0)
    
    #cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
   # cv.imshow("close",closed)
    #print("shape",closed.dtype)
   # print("shape",gray.dtype)
   # Roi_extract = np.multiply(closed,gray)
    ret, binary = cv.threshold(image_blur, 10,255,cv.THRESH_BINARY)
    #cv.imshow("binary image",binary)
    
    cloneImage, contours, heriachy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    """
    for i,contour in enumerate(contours):
        #cv.drawContours(image,contours,i,(0,0,255),2)
        cv.drawContours(image,contours,i,(0,255,255),-1)#-1 是填充轮廓
        cv.drawContours(background,contours,i,3,-1)
    """
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (20,20))
    closed = cv.morphologyEx(cloneImage, cv.MORPH_CLOSE, kernel)/255
    cv.imshow("Roi_extract_area",closed)
    
    return closed
 #  print(np.min(Roi_extract))
    
    #cv.imshow("Roi_extract", Roi_extract)
   # print(np.mean(Roi_extract))
   
def BACKGROUND(mat,image_initial):
    row, col = image_initial.shape[:2]
    inver_mat = np.power(mat-1,2)
    #cv.imshow("inver_mat",inver_mat)
    ROI = inver_mat*image_initial
    
    Effective_pixel_number_background =np.float32(0)
    Sum_pixel_value_background =np.float32(0)
    Mean = np.float32(0)
    
    for h in range(row):
        for w in range(col):
            if ROI[h,w]>0:
                Effective_pixel_number_background= Effective_pixel_number_background+1
                Sum_pixel_value_background = Sum_pixel_value_background+ROI[h, w]
                
    Mean =Sum_pixel_value_background/Effective_pixel_number_background
    #cv.imshow("ROI",inver_mat)
    #print(inver_mat[400,400])
    return Mean 
    
def SUM_PIXEL_VALUE(mat,image_initial,background):
  
    
    row, col = image_initial.shape[:2]
    
    Effective_pixel_number =np.int32(0)
    Sum_pixel_value=np.float32(0)
    

    Mean = np.float32(0)

    ROI=mat*image_initial
    
    for h in range(row):
        for w in range(col):
            if ROI[h,w]>0:
                
                Effective_pixel_number = Effective_pixel_number+1
                Sum_pixel_value = Sum_pixel_value+ROI[h, w]-background
                
                 
    Mean = Sum_pixel_value/Effective_pixel_number
    
    return Mean,Sum_pixel_value,Effective_pixel_number

def STD(mat,image_initial,Effective_pixel_number,background):
    
    total = []
    row, col = image_initial.shape[:2]
    ROI = mat*image_initial
    
    
    for h in range(row):
        for w in range(col):
            if ROI[h,w] > background:
                total.append( ROI[h,w]-background)
                
    return np.std(total)


def Creat_RGB_HIST(image):
    h, w = image.shape
    rgbHist = np.zeros([16*16*16, 1], np.float32)  # must be float32 
    bsize =256/16
    for row in range(h):
        for col in range(w):
            b = image[row, col ]
            g = image[row, col ]
            r = image[row, col ]
            index = np.int(b/bsize)*16*16 +np.int(g/bsize)*16 +np.int(r/bsize)
            rgbHist[np.int(index),0] = rgbHist[np.int(index),0] +1
    return rgbHist

def IMAGE_CHECK(image1,image2):
    hist1 =  Creat_RGB_HIST(image1)
    hist2 =  Creat_RGB_HIST(image2)
    
    compare1 = cv.compareHist(hist1,hist2, cv.HISTCMP_BHATTACHARYYA)
    compare2 = cv.compareHist(hist1,hist2, cv.HISTCMP_CORREL)
    compare3 = cv.compareHist(hist1,hist2, cv.HISTCMP_CHISQR)
    
    return  compare1 , compare2 , compare3 

######################### WRITE Excel ######################### 

def WRITE_EXCEL(dirs,file_name, Name_excel, Mean_excel, Sum_pixel_value_excel, Effective_pixel_number_excel, Std_excel, Fwhm_excel, Remarks_excel):
    
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('Energy calibration',cell_overwrite_ok=True)
    
    row0 = ["No","Name","Sum_pixel_value","Effective_pixel_number","Mean","Std","FWHM","Remarks"]

    #first line
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
        
    for i in range(0,len(Name_excel)):
        sheet1.write(i+1, 0, i+1, set_style('Times New Roman',220,False))
        sheet1.write(i+1, 1,Name_excel[i],set_style('Times New Roman',220,False))
        sheet1.write(i+1,2,Mean_excel[i],set_style('Times New Roman',220,False))       
        sheet1.write(i+1,3,Sum_pixel_value_excel[i],set_style('Times New Roman',220,False))
        sheet1.write(i+1,4,Effective_pixel_number_excel[i],set_style('Times New Roman',220,False))   
        sheet1.write(i+1,5,Std_excel[i],set_style('Times New Roman',220,False))       
        sheet1.write(i+1,6,Fwhm_excel[i],set_style('Times New Roman',220,False))
        sheet1.write(i+1,7,Remarks_excel[i],set_style('Times New Roman',220,False))

    f.save(dirs+file_name)

##################################################
def FILE_CHECK(dirs,file_type): 
    
    File_list = os.listdir(dirs)
    name_list=[]
    for file in File_list:
        if os.path.splitext(file)[1] == file_type:
            t = os.path.splitext(file)[0]+file_type
            #print(t)   
            name_list.append(t)
    return name_list


##################################################  main  ##################################################
if __name__=="__main__":  
    t1 = cv.getTickCount()  
    filename = "C:/Users/myshi/Desktop/PythonSHHG/image_load/1.png"
    filename_blank = "C:/Users/myshi/Desktop/PythonSHHG/image_load/1132_20190110__Manta_NF_afterPM 201901-10 19.23.51.png"
    
    src_8bit = cv.imread(filename,cv.IMREAD_ANYCOLOR)
    src_initial= cv.imread(filename,cv.IMREAD_UNCHANGED)
    blank_image = cv.imread(filename_blank,cv.IMREAD_ANYCOLOR)
    
    cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)
    cv.imshow("input image",src_initial)
    
    
    ##################################################
    image_8bit = src_8bit[100:900,100:1000]
    image_initial = src_initial[100:900,100:1000]
    image_filename_blank = blank_image[100:900,100:1000]
    
    row, col = image_initial.shape[:2]
    
        
    HISTCMP_BHATTACHARYYA, HISTCMP_CORREL, HISTCMP_CHISQR = IMAGE_CHECK(image_8bit, image_filename_blank)  #"巴氏距离：, 相关性：, 卡方：
     
    print("HISTCMP_BHATTACHARYYA:",HISTCMP_BHATTACHARYYA)
    print("HISTCMP_CORREL:       ",HISTCMP_CORREL)
    print("HISTCMP_CHISQR:       ",HISTCMP_CHISQR)
    print("\n")
    
    
    mat = CONTOURS(image_8bit)
    
    background = BACKGROUND(mat,image_initial)
    
    Mean,Sum_pixel_value,Effective_pixel_number = SUM_PIXEL_VALUE(mat,image_initial,background)
    
    
    Std = STD(mat,image_initial,Effective_pixel_number,background) 
    FWHM =2.355*Std 
    print("Mean",Mean)
    print("Sum_pixel_value",Sum_pixel_value)
    print("Effective_pixel_number",Effective_pixel_number)
    print("Std",Std)
    print("FWHM",FWHM)
    
    
    #WRITE_EXCEL(dirs, file_name, Name_excel, Mean_excel, Sum_pixel_value_excel, Effective_pixel_number_excel, Std_excel, Fwhm_excel,Remarks_excel)
       
    
    ##################################################
    t2 = cv.getTickCount()
    Running_time = (t2-t1)/cv.getTickFrequency()
    print("Running time:%s s"%Running_time)
    cv.waitKey(0)
    cv.destroyAllWindows()
