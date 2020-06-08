import sys
import cv2 as cv
import numpy as np
from collections import deque
from tensorflow.python.keras.models import load_model


def get_contour_precedence(contour, cols):                  #정렬 알고리즘 함수
    origin = cv.boundingRect(contour)
    return origin[1] * cols + origin[0]


letters = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',
10:'A',11:'B',12:'C',13:'D',14:'E',15:'F',16:'G',17:'H',18:'I',19:'J',20:'K',21:'L',22:'M',23:'N',24:'O',25:'P',26:'Q',27:'R',28:'S',29:'T',30:'U',
31:'V',32:'W',33:'X',34:'Y',35:'Z',
36:'a',37:'b',38:'d',39:'e',40:'f',41:'g',42:'h',43:'n',44:'q',45:'r',46:'t'}



img_color = cv.imread('./testimg/test9.jpg', cv.IMREAD_COLOR)         #이미지 파일 불러오기
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)        #그레이스케일 파일로 전환


ret,img_binary = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)      #그레이스케일 이미지를 이진화 -> 바이너리이미지(흑백)

kernel = cv.getStructuringElement( cv.MORPH_RECT, ( 5, 5 ) )        #이진화 결과 공백메꾸기
img_binary = cv.morphologyEx(img_binary, cv. MORPH_CLOSE, kernel)


"""
cv.imshow('digit', img_binary)      
cv.waitKey(0)
"""

#숫자경계박스 말고 하나만 보이는거 구현예정



contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL,         #컨투어 검출    #RETR_EXTERNAL->가장 외곽에 있는 컨투어 return
                        cv.CHAIN_APPROX_SIMPLE)




#contours.sort(key = lambda x:get_contour_precedence(x, img_binary.shape[1]))    #정렬 알고리즘
                                                                                #img_binary.shape는 이미지파일의 모양을 return
                                                                                #3개의 값이 return 되는데 Y축, X축, 컬러채널 수를 의미
                                                                                #img_binary.shape[1]이므로 X축을 인자로 사용(cols로 전달)

text = open('output_text.txt','w')


for contour in contours:

    x, y, w, h = cv.boundingRect(contour)                                   #숫자별 경계박스, 4차원배열으로 사각형의정보 return
                                                                            #boundingRect : contour에 외접하는 사각형 return


    length = max(w, h) + 60                                                 #컨투어로 이미지 근사화(숫자별로 분리)
    img_digit = np.zeros((length, length, 1),np.uint8)

    new_x,new_y = x-(length - w)//2, y-(length - h)//2                      #숫자가 이미지의 정중앙에 오도록 경계박스 시작위치 조정


    img_digit = img_binary[new_y:new_y+length, new_x:new_x+length]          #바이너리 이미지를 가져와서 img_digit에 넣는다

    kernel = np.ones((5, 5), np.uint8)
    img_digit = cv.morphologyEx(img_digit, cv.MORPH_DILATE, kernel)         #인식이 잘 되도록 팽장모폴로지 연산


    #cv.imshow('digit', img_digit)
    #cv.waitKey(0)

    model = load_model('emnist_cnn_model_balanced.h5')                                          #학습된 모델 호출

    img_digit = cv.resize(img_digit, (28, 28), interpolation=cv.INTER_AREA) #이미지 크기를 학습된 모델사이즈로 맞춘다(28 X 28)

    img_digit = img_digit / 255.0                                           #이미지 픽셀 범위도 0 ~ 1 사이로

    img_input = img_digit.reshape(1, 28, 28, 1)                             #이미지 형태 변환
    predictions = model.predict(img_input)                                  #PREDICTIONS -> 예측값


    number = np.argmax(predictions)                                         #argmax 함수 -> softmax를 숫자로 변환
    print(letters[number])                                                           #숫자 출력
    text.write(letters[number])



    cv.rectangle(img_color, (x, y), (x+w, y+h), (255, 255, 0), 2)           #이미지에 대한 사각형 그리기
    location = (x + int(w *0.5), y - 10)                                    #이미지수 위에 인식된 숫자를 적어줍니다
    font = cv.FONT_HERSHEY_COMPLEX  
    fontScale = 1.2
    cv.putText(img_color, str(letters[number]), location, font, fontScale, (255,0,0), 2)




text.close()

#cv.drawContours(img_color,contours,-1,(0,255,0),3)                          #컨투어 겉면에 그리기
img_color_resized = cv.resize(img_color,(960,960))
cv.imshow('result', img_color_resized)
cv.waitKey(0)





