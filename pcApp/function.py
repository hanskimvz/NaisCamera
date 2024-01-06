import time, os, sys
import cv2 as cv
import tkinter as tk



class LoadStreams: 
    def __init__(self, url, img_size=640):
        self.img_size = img_size
        self.capture = None
        self.Running = True

        self.url = url

        self.cap = cv.VideoCapture(url)
        assert self.cap.isOpened(), 'Failed to open %s' % s
        w   = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        h   = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv.CAP_PROP_FPS) % 100
        _, self.imgs = self.cap.read()  # guarantee first frame
    
    def run(self):
        showHelp = True
        showFullScreen = False
        helpText = "'Esc' to Quit, 'H' to Toggle Help, 'F' to Toggle Fullscreen"
        info = self.url + ':' + self.sn
        font = cv.FONT_HERSHEY_PLAIN
        fontsize = 5.0
        if self.cap.isOpened():
            width  = self.cap.get(3)   # float `width`
            if width < 800:
                fontsize = 3.0

        while self.cap.isOpened() and self.Running:
            ret, frame = self.cap.read()
            if showHelp:
                cv.putText(frame, helpText, (11,20), font, 1.0, (32,32,32), 4, cv.LINE_AA)
                cv.putText(frame, helpText, (10,20), font, 1.0, (240,240,240), 1, cv.LINE_AA)
                
                cv.putText(frame, info, (40,200), font, fontsize, (32,32,32), 4, cv.LINE_AA)
                cv.putText(frame, info, (38,200), font, fontsize, (240,240,240), 1, cv.LINE_AA)        


            cv.imshow(self.url, frame)
            ch = cv.waitKey(1) &0xFF
            if ch == 27 or ch == ord('q') or ch == ord('Q'):
                self.Running = False
                break
            elif ch == ord('H') or ch == ord('h'):
                showHelp = not showHelp
            elif ch == ord('F') or ch == ord('f') :
                showFullScreen = not showFullScreen
                if showFullScreen == True: 
                    # width, height  = 1920, 1080
                    cv.setWindowProperty(self.url, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                else :
                    width, height = 640, 320
                    cv.setWindowProperty(self.url, cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL) 
                    cv.resizeWindow(self.url, width, height)
        self.cap.release()
        cv.destroyAllWindows()

    def stop(self):
        self.Running = False
        print("stop!")
        self.cap.release()
        cv.destroyAllWindows()



def show_video(url=''):
    Running = True
    showHelp = True
    showFullScreen = False
    helpText = "'Esc' to Quit, 'H' to Toggle Help, 'F' to Toggle Fullscreen"
    # helpText = "'你好' to Quit, 'H' to Toggle Help, 'F' to Toggle Fullscreen"
    font = cv.FONT_HERSHEY_PLAIN
    height = 320
        
    cap = cv.VideoCapture(url)
    cv.namedWindow(url, cv.WINDOW_NORMAL)
    cv.resizeWindow(url, 640, height)

    fontsize = 5.0
    if cap.isOpened():
        width  = cap.get(3)   # float `width`
        if width < 800:
            fontsize = 3.0

    cap.set(cv.CAP_PROP_BUFFERSIZE,1)
    while Running :
        # t = time.time()
        ret, image= cap.read()
        
        if not ret :
            break

        if showHelp:
            cv.putText(image, helpText, (11,20), font, 1.0, (32,32,32), 4, cv.LINE_AA)
            cv.putText(image, helpText, (10,20), font, 1.0, (240,240,240), 1, cv.LINE_AA)
            
        cv.imshow(url, image)
        ch = cv.waitKey(1) &0xFF
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            Running = False
            break
        elif ch == ord('H') or ch == ord('h'):
            showHelp = not showHelp
        elif ch == ord('F') or ch == ord('f') :
            showFullScreen = not showFullScreen
            if showFullScreen == True: 
                # width, height  = 1920, 1080
                cv.setWindowProperty(url, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            else :
                width, height = 640, 320
                cv.setWindowProperty(url, cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL) 
                cv.resizeWindow(url, width, height)
            
            # cv.resizeWindow(url, width, height)
        # print (1/(time.time()-t))
    cap.release()
    cv.destroyAllWindows()        