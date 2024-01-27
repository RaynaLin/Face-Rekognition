# Face-Rekognition
Amazon AWS Rekognition project

![IndexPage](./public/face_rekognition_GUI.png)

## Description
這是透過Amazon AWS的Face Rekognition Service所寫的專案，
假設使用情境大樓，辨識目標是否為住戶。

## 開發工具
 - Python 3.10
 - numpy 1.24.3
 - pillow 9.4.0
 - boto3 1.34.28
 - opencv-python 4.9.0.80
 - tk 8.6.12

## 使用說明

請先下載適用於Python 的AWS開發套件(Boto3)
`pip install boto3`

透過open-cv來進行讀取、顯示、儲存圖像
`pip install opencv-python`

透過PIL進行轉檔
`pip install Pillow`

會使用到GUI介面
`pip install tk`

1. 需申請AWS帳號
2. 利用IAM Service創建使用者，許可政策為AdministratorAccess及AmazonS3FullAccess並建立存取金鑰
3. 利用GUI介面操作，以下為按鈕介紹:
 - 選取照片按鈕，選取目標圖檔
 - 開始辨識按鈕，將目標圖檔與來源圖檔做辨識
 - 顯示辨識結果照片，若成功辨識會在目標的臉出現綠色框，若不是則不會出現綠色框
 - 顯示值，將會顯示相似度、信賴度、此人是否為住戶

## 參考文件
- AWS_Amazon Rekognition_開發人員指南：https://docs.aws.amazon.com/zh_tw/rekognition/latest/dg/faces-detect-images.html
