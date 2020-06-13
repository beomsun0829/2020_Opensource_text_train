import cv2
f=open("N좌표값.txt", 'w')
i=0
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global i
        i += 1
        print("N" ,i, "x:", x ," y:", y) # 이벤트 발생한 마우스 위치 출력
        data=('N %d, x: %d , y: %d\n' %(i,x,y))
        f.write(data)
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("N", i, "x:", x, " y:", y)  # 이벤트 발생한 마우스 위치 출력
        data = ('N %d, x: %d , y: %d\n' % (i, x, y))
        f.write(data)





image = cv2.imread("C:\\Users\\demy1\\Pictures\\image\\N-Sector.png", cv2.IMREAD_ANYCOLOR)
dst = cv2.resize(image, dsize=(1115, 1050), interpolation=cv2.INTER_AREA)
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_callback)
while(True):

    cv2.imshow('image', dst)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:    # ESC 키 눌러졌을 경우 종료
        print("ESC 키 눌러짐")
        break
cv2.destroyAllWindows()
f.close()