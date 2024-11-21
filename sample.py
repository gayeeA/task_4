import cv2 
abo_image = cv2.imread('blood cell.jpg')
gray = cv2.cvtColor(abo_image,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
val1,threshold = cv2.threshold(blur,120,255,cv2.THRESH_BINARY)
contour,val2 = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contour_length = len(contour)
if(contour_length<50):
    print('O')
elif(50 <= contour_length < 100):
    print('A')
elif(100 <= contour_length < 150):
    print('B')
else:
    print('AB')
cv2.waitKey(0)
cv2.destroyAllWindows()