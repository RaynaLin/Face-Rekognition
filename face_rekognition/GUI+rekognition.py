'''
=========================================
###Load packages
=========================================
'''
import numpy as np
import boto3, os , glob 
import pandas as pd
import csv
import cv2
import time
import io
from PIL import Image, ImageTk, ImageDraw

'''
=========================================
###confirm user
=========================================
'''
with open(r'your credentials file rode') as input:
    reader = csv.reader(input)
    for line in reader:
        print(line)
        access_key_id = line[2]
        secret_access_key = line[3]

print(access_key_id)
print(secret_access_key)

'''
=========================================
###compareface rekognition
=========================================
'''

def compare_faces(sourceFile, targetFile): 
    
    client = boto3.client('rekognition',
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      region_name='us-east-1')
 

    imageSource=open(sourceFile,'rb') 
    imageTarget=open(targetFile,'rb')
    response=client.compare_faces(SimilarityThreshold=80, 
                                  SourceImage={'Bytes': imageSource.read()}, 
                                  TargetImage={'Bytes': imageTarget.read()}) 

    for faceMatch in response['FaceMatches']:
            similarity = faceMatch['Similarity']
            confidence = faceMatch['Face']['Confidence']
    if similarity > 80:      
        print('Similarity:' + str(similarity))    #can only concatenate str (not "float") to str
        print('Confidence:' + str(confidence))
        determine = 'This person is a resident of the building.'
        print(determine)
                
    else:
        print('Similarity:' + str(similarity))    
        print('Confidence:' + str(confidence))
        determine = 'This person is not a resident of the building.'
        print(determine)

    path = 'output.txt'
    f = open(path, 'w')
    f.write('Similarity:' + str(similarity) + '\n')
    f.write('Confidence:' + str(confidence)+ '\n')
    f.write(determine)
    f.close()  
    
    imageSource.close() 
    imageTarget.close()
    
    return response 

def compute(response):    
    position = 0
    similarity = 0    
    if (len(response['FaceMatches']) == 1):
        position = response['FaceMatches'][0]['Face']['BoundingBox']
        similarity = response['FaceMatches'][0]['Similarity']
    return similarity, position


def show_faces(position, targetFile):
    with open(targetFile, 'rb') as image:
        targetFile = image.read()
    stream = io.BytesIO(targetFile)
    image = Image.open(stream)
    
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    left = imgWidth * position['Left']
    top = imgHeight * position['Top']
    width = imgWidth * position['Width']
    height = imgHeight * position['Height']

    points = (
        (left, top),
        (left + width, top),
        (left + width, top + height),
        (left, top + height),
        (left, top)
    )
    draw.line(points, fill='#00d400', width=3)

    image.save('../face_rekognition/result.jpg')

def main(): 
    source_file='../imgs/resident pic/09.jpg'
    target_file='../imgs/compare pic/group.jpg'
    response = compare_faces(source_file, target_file)
    sim, pos = compute(response)
    show_faces(pos,target_file)    
    # print("Face matches: " + str(face_matches)) 

if __name__ == "__main__": 
    main()

'''
=========================================
###Load GUI packages
=========================================
'''

from tkinter import messagebox, filedialog, ttk, Frame
import tkinter as tk

'''
=========================================
###GUI interface
=========================================
'''
   
window = tk.Tk()
window.title('人臉辨識系統')
align_mode = 'nswe'
pad = 5

div_size = 200
img_size = div_size * 2
div1 = tk.Frame(window,  width=img_size , height=img_size , bg='#EED6D3')
div2 = tk.Frame(window,  width=img_size , height=img_size , bg='#EED6D3')
div3 = tk.Frame(window,  width=div_size , height=div_size , bg='#EED6D3')
div4 = tk.Frame(window,  width=div_size , height=div_size , bg='#EED6D3')


div1.grid(column=0, row=0, padx=pad, pady=pad)
div2.grid(column=1, row=0, padx=pad, pady=pad)
div3.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)
div4.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)

def define_layout(obj, cols=1, rows=1):   
    def method(trg, col, row):
       for c in range(cols):    
            trg.columnconfigure(c, weight=1)
       for r in range(rows):
            trg.rowconfigure(r, weight=1)
    if type(obj)==list:        
        [ method(trg, cols, rows) for trg in obj ]
    else:
        trg = obj
        method(trg, cols, rows)
        

#div4 - buttonA選照片
#選取
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img


photoA = tk.Label(div1)
def select_image():
    global sfname

    sfname = filedialog.askopenfilename(title='選擇',filetypes=[('All Files','*'),("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif")])
    
    im = Image.open(sfname)         #讀取圖片 
    im = cv_imread(sfname) 
    cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)                           
    img = Image.fromarray(cv2image)                  #實現array到image的轉換  
    img = img.resize((round(img.width * 300 / img.height), 300)) 
    imgtk = ImageTk.PhotoImage(image=img)            #轉換成Tkinter可以用的圖片    
    image_main = tk.Label(div1, image=imgtk)         #宣告標籤並且設定圖片
    image_main['height'] = img_size
    image_main['width'] = img_size
    image_main.grid(column=0, row=0, sticky=align_mode)
    
    photoA.imgtk = imgtk
    photoA.configure(image=imgtk)


#div2 - buttonB顯示結果照片
photoB = tk.Label(div2)
def finishreg_photo():
    im = Image.open('.../face_rekognition/result.jpg') 
    im = cv_imread('../face_rekognition/result.jpg') 
    cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)                            
    img = Image.fromarray(cv2image)                 
    img = img.resize((round(img.width * 300 / img.height), 300)) 
    imgtk = ImageTk.PhotoImage(image=img)               
    image_main = tk.Label(div2, image=imgtk)        
    image_main['height'] = img_size
    image_main['width'] = img_size
    image_main.grid(column=0, row=0, sticky=align_mode)
    
    photoB.imgtk = imgtk
    photoB.configure(image=imgtk)


# div3 - text
txtlst = []
f = open('output.txt', 'r')
for line in f.readlines():
    txtlst.append(line)
f.close

def text():
    lbl_title1 = tk.Label(div3, text= txtlst[0], bg='#EED6D3', fg='black')
    lbl_title2 = tk.Label(div3, text= txtlst[1], bg='#EED6D3', fg='black')
    lbl_title3 = tk.Label(div3, text= txtlst[2], bg='#EED6D3', fg='black')
    
    lbl_title1.grid(column=0, row=0, sticky=align_mode)
    lbl_title2.grid(column=0, row=1, sticky=align_mode)
    lbl_title3.grid(column=0, row=2, sticky=align_mode)


# 設定按鈕 (div4有兩個按鈕)  
bt1 = tk.Button(div4, text='選取照片', bg='#67595E', fg='white',command = select_image) #選取照片
bt2 = tk.Button(div4, text='開始辨識', bg='#67595E', fg='white',command =main())
bt3 = tk.Button(div4, text='顯示辨識結果照片', bg='#67595E', fg='white',command =finishreg_photo) 
bt4 = tk.Button(div4, text='顯示值', bg='#67595E', fg='white',command =text) #辨識及顯示值

bt1.grid(column=0, row=0, sticky=align_mode)
bt2.grid(column=0, row=1, sticky=align_mode)
bt3.grid(column=0, row=2, sticky=align_mode)
bt4.grid(column=0, row=3, sticky=align_mode)
#bt1['command'] = lambda : get_size(window, image_main, im)



define_layout(window, cols=1, rows=5)
define_layout([div1, div2, div3, div4])

window.mainloop()
