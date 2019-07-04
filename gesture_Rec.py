import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
mouse = Controller()
app=wx.App(False)
sx, sy=wx.GetDisplaySize()
(camx,camy)=(320,240)
low = np.array([100,20,30])#green#np.array([65,80,70])#65,60,60#blue=====>110,50,50
high = np.array([130,255,255])#green#np.array([110,120,60])#blue=====>130,255,255
cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)
kernalOpen=np.ones((10,10))
kernalClose=np.ones((10,10))
openx,openy,openw,openh=(0,0,0,0)
mLocationOld=np.array([0,0])
mouseLoc=np.array([0,0])
DampingFactor=1.01

pinchFlag=0

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
	if(len(conts)==2):
		if(pinchFlag==1):
			pinchFlag=0
			mouse.release(Button.left)
		x1,y1,w1,h1=cv2.boundingRect(conts[0])
		x2,y2,w2,h2=cv2.boundingRect(conts[1])
		cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,100),2)
		cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,100),2)
		cx1=int(x1+w1/2)
		cx2=int(x2+w2/2)
		cy1=int(y1+h1/2)
		cy2=int(y2+h2/2)
		cv2.line(img,(cx1,cy1),(cx2,cy2),(0,0,255),2)
		cx=int((cx1+cx2)/2)
		cy=int((cy1+cy2)/2)
		cv2.circle(img,(cx,cy),2,(255,0,0),2)
		roi = img[x1:x1+w1, y1:y1+h1]
		# print(roi)
		print(cx*sx/camx,cy*sy/camy)
		mouseLoc=mLocationOld+((cx,cy)-mLocationOld)/DampingFactor
		mouse.position=(int(sx-(mouseLoc[0]*sx/camx)),int(mouseLoc[1]*sy/camy))
		# while (mouse.position==(int(cx*sx/camx),int(cy*sy/camy))):
		# 	pass

		openx,openy,openw,openh=cv2.boundingRect(np.array([[[x1,y1],[x1+w1,y1+h1],[x2,y2],[x2+w2,y2+h2]]]))
		mLocationOld = mouseLoc
	elif(len(conts)==1):
		x,y,w,h=cv2.boundingRect(conts[0])
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,100),2)     
		cx=int(x+w/2)
		cy=int(y+h/2)              
		cv2.circle(img,(cx,cy),int((w+h)/4),(255,255,0),2)
		# while(mouse.position==(int(cx*sx/camx),int(cy*sy/camy))):
		# 	pass
		mouseLoc=mLocationOld+((cx,cy)-mLocationOld)/DampingFactor
		mouse.position=(int(sx-(mouseLoc[0]*sx/camx)),int(mouseLoc[1]*sy/camy))

		if(pinchFlag==0):
			if (abs((w*h-openw*openh)/(w*h))<0.2):				
				# cv2.rectangle(img,(openx,openy),(openx+openw,openy+openh),(0,255,255),2)
				pinchFlag=1
				mouse.press(Button.left)
				openx,openy,openw,openh=(0,0,0,0)
		mLocationOld = mouseLoc
	cv2.imshow("maskOpen",maskOpen)
	# cv2.imshow("maskClose",maskClose)
	# cv2.imshow("mask",mask)
	cv2.imshow("orignal",img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	pass
