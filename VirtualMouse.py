import cv2
import mediapipe
import HandGestureRecognition as hgr
import time
import numpy as np
import pyautogui


def main():
    pTime = 0
    cTime = 0
    wCam, hCam = 640,480
    frameR = 20
    smoothvalue = 5
    plocX,plocY = 0,0
    clocX,clocY = 0,0
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = hgr.handDetector()
    wScr, hScr = pyautogui.size()
   
    while 1:
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
        
        #findHand 
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if len(lmlist) != 0:
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]
            #print(x1, y1, x2, y2)
            #check which fingers are up
            fingers = detector.fingersUp()
            cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255), 2)
            #print(fingers)           
            
            #moving mode
            if fingers[1] == 1 and fingers[2] == 0 and fingers[3]== 0 and fingers[0] == 0 and fingers[4] ==0:
                #convert
                x3 = np.interp(x1, (frameR,wCam-frameR),(frameR,wScr-frameR))
                y3 = np.interp(y1, (frameR,hCam-frameR),(frameR,hScr-frameR))
                #smoothen values:
                clocX = plocX +(x3 - plocX) / smoothvalue
                clocY = plocY +(y3 - plocY) / smoothvalue
                pyautogui.moveTo(wScr - clocX,clocY)
                cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
                plocX, plocY = clocX, clocY
            
            #left click
            if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1 and fingers[3] == 0 and fingers[4]==0:
                length ,img, lineInfo = detector.findDistance(8,4,img)
                #print(length)
                if length<30:
                    cv2.circle(img,(lineInfo[4],lineInfo[5]),10,(0,255,255),cv2.FILLED)
                    pyautogui.click()
            
            #rightclick
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[0] == 0 and fingers[4] == 0:
                length ,img, lineInfo = detector.findDistance(8,12,img)
                #print(length)
                if length<30:
                    cv2.circle(img,(lineInfo[4],lineInfo[5]),10,(0,255,255),cv2.FILLED)
                    pyautogui.rightClick()
            
            #double click
            if fingers[1] == 0 and fingers[2] == 0 and fingers[0] == 1 and fingers[3] == 0 and fingers[4]==0:
                length ,img, lineInfo = detector.findDistance(4,2,img)
                if length<120:
                    cv2.circle(img,(lineInfo[4],lineInfo[5]),10,(255,255,0),cv2.FILLED)
                    pyautogui.doubleClick()
            
            #scrolling
            if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 1 and fingers[4]==0:
                length ,img, lineInfo = detector.findDistance(8,16,img)
                #length2 , img, lineInfo = detector.findDistance(12,16,img)
                #print(length)
                if length<50:
                    cv2.circle(img,(lineInfo[4],lineInfo[5]),10,(255,0,255),cv2.FILLED)
                    pyautogui.scroll(1)
                    
            
            if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 1 and fingers[4]==1:
                length ,img, lineInfo = detector.findDistance(8,20,img)
                 #length2 , img, lineInfo = detector.findDistance(12,16,img)
            #     #print(length)
                if length>50:
                    cv2.circle(img,(lineInfo[4],lineInfo[5]),10,(255,0,255),cv2.FILLED)
                    pyautogui.scroll(-1)
                    
            
            

        cTime = time.time()
        fps = 1 / (cTime - pTime)   
        img = cv2.flip(img,1)
        cv2.imshow("Image", img)
        


if __name__ == "__main__":
    main()
