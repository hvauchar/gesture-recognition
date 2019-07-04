import cv2
import numpy as np 
low = np.array([33,80,40])#65,60,60
high = np.array([102,255,255])
cam = cv2.VideoCapture(0)
kernalOpen=np.ones((5,5))
kernalClose=np.ones((20,20))
while True:
	ret, img=cam.read()
	#qimg=cv2.resize(img,(340,220))
	#convert BGR to HSV
	imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(imgHSV, low, high)
	#morphology
	maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernalOpen)
	maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernalClose)
	maskFinal=maskClose
	image, conts, h = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(img, conts,-1,(255,0,0),3)
	for i in range(len(conts)):
		x,y,w,h = cv2.boundingRect(conts[i])
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
		cv2.putText(img = img, text = str(i+1), org = (x+w, y+h), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.5, 
	                color = (0, 0, 255))
	# cv2.imshow("maskOpen",maskOpen)
	# cv2.imshow("maskClose",maskClose)
	# cv2.imshow("mask",mask)
	cv2.imshow("orignal",img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	pass