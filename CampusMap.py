import cv2
import sqlite3

con, cur = None, None
row=None
data1, data2, data3, data4,data5,data6="","","","","",""

con=sqlite3.connect("PyCampusMapDB")    #DB연결
cur=con.cursor()
class Building:     #건물 정보 객체
    def setdata(self,bd_code,bd_name,big_x,big_y,small_x,small_y):
        self.bd_code=bd_code    #건물번호
        self.bd_name=bd_name    #건물이름
        self.big_x=big_x    #큰 지도 이미지 건물 x좌표
        self.big_y=big_y    #큰 지도 이미지 건물 y좌표
        self.small_x=small_x    #작은 지도 이미지 건물 x좌표
        self.small_y=small_y    #작은 지도 이미지 건물 y좌표

def findBD(bd_code,B1):
    cur.execute("SELECT * FROM userTable WHERE userTable.BD_Code =='%s'" %bd_code)  #DB에서 검색한 건물 이름이 있으면
    row=cur.fetchone()  #검색된 한 행을 가져옴
    data1=row[0]
    data2=row[1]
    data3=row[2]
    data4=row[3]
    data5=row[4]
    data6=row[5]
    B1.setdata(data1,data2,data3,data4,data5,data6)     #B1에 입력

def Show_Location(B1):  #큰 지도에서 위치 입력
    vpos=B1.big_y-70    #이미지 합성할 y좌표 확인
    hpos=B1.big_x-40    #이미지 합성할 x좌표 확인

    img1=cv2.imread("map_b.jpg")     #지도 이미지
    img2=cv2.imread("pin4.png")      #핀 이미지
    img1=cv2.resize(img1,(1115, 1050))      #지도 이미지 크기 설정
    img2 = cv2.resize(img2, (70, 70))       #핀 이미지 크기 설정
    rows, cols, channels = img2.shape   #핀 이미지의 크기 확인
    roi=img1[vpos:rows+vpos, hpos:cols+hpos]    #이미지 합성할 공간 확보

    img2gray=cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)     #핀 이미지 설정
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)     #핀 이미지 설정
    mask_inv=cv2.bitwise_not(mask)      #핀 이미지 설정

    img1_bg = cv2.bitwise_and(roi,roi,mask=mask_inv)    #배경 이미지(지도) 설정

    img2_fg = cv2.bitwise_and(img2,img2,mask=mask)  #재료 이미지(핀) 설정

    dst= cv2.add(img1_bg, img2_fg)  #이미지 합성
    img1[vpos:rows+vpos, hpos:cols+hpos] = dst

    cv2.imshow('CampusMap', img1)   #이미지 출력
    cv2.waitKey(0)      #무한 대기
    cv2.destroyAllWindows()     #이미지 출력창 닫기

def Show_DetLocation(B1):
    vpos = B1.small_y - 85
    hpos = B1.small_x - 18
    if(B1.bd_code[0]=='N'):  #건물이 N구역이면
        img1 = cv2.imread("N-sector.png")
    elif (B1.bd_code[0] == 'E'):    #건물이 E구역이면
        img1 = cv2.imread("E-sector.png")
    elif (B1.bd_code[0] == 'S'):    #건물이 S구역이면
        img1 = cv2.imread("S-sector.png")

    img2 = cv2.imread("pin4.png")
    img1 = cv2.resize(img1, (1115, 1050))
    img2 = cv2.resize(img2, (100, 100))
    rows, cols, channels = img2.shape
    roi = img1[vpos:rows + vpos, hpos:cols + hpos]

    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)

    dst = cv2.add(img1_bg, img2_fg)
    img1[vpos:rows + vpos, hpos:cols + hpos] = dst

    cv2.imshow('SectorMap', img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    bd_code=input("건물번호 입력: ")  #건물번호 입력
    B1=Building()   #객체 선언
    findBD(bd_code,B1)  #건물 검색
    print(B1.bd_code, '의 건물명은', B1.bd_name, '입니다.')
    menu1=int(input("지도를 출력하려면 1번을 누르세요\n"))
    if menu1 == 1:
        Show_Location(B1)   #큰 지도에서 위치 출력

    menu2=int(input("자세한 위치를 보려면 2번을 누르세요\n"))
    if menu2 == 2:
        Show_DetLocation(B1)     #작은 지도에서 위치 출력