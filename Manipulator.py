import cv2
import numpy as np

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)
# To use a video file as input 
# cap = cv2.VideoCapture('filename.mp4')

while True:
    # Read the frame
    ret, bkg = cap.read()
    gray = cv2.cvtColor(bkg, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # First create the image with alpha channel
    newbkg = cv2.cvtColor(bkg, cv2.COLOR_RGB2RGBA)
    # Then assign the mask to the last channel of the image
    newbkg[:, :, 3] = .2

    mask = 0
    for (x, y, w, h) in faces:
        maskW, maskH = int(w*1.25), int(h*1.25)
        x,y = int(x-maskW*.125), int(y-maskH*.125)
        mask = cv2.resize(cv2.imread('images/fox.png', cv2.IMREAD_UNCHANGED), (maskW, maskH), interpolation = cv2.INTER_AREA)

        #replace all transparent pixels with the appropriate pixels
        for i in range(maskH):
            for j in range(maskW):
                if(mask[i,j,3] == 0):
                    try:
                        mask[i,j,0] = newbkg[y+i,x+j,0]
                        mask[i,j,1] = newbkg[y+i,x+j,1]
                        mask[i,j,2] = newbkg[y+i,x+j,2]
                    except:
                        pass

        #use image blending when there is space to add the filter
        try:
            added_image = cv2.addWeighted(newbkg[y:y+maskH,x:x+maskW,:],0,mask[:,:,:],1,0)
            newbkg[y:y+maskH,x:x+maskW] = added_image
        except cv2.error:
            pass

        # # normalize alpha channels from 0-255 to 0-1
        # alpha_bk = newbkg[y:y+h,x:x+w,3] / 255.0
        # alpha_fg = mask[:,:,3] / 255.0

        # # set adjusted colors
        # for c in range(0, 3):
        #     newbkg[:,:,c] = alpha_fg * mask[:,:,c] + alpha_bk * newbkg[:,:,c] * (1-alpha_fg)

        # # set adjusted alpha and denormalize back to 0-255
        # newbkg[:,:,3] = (1 - (1-alpha_fg)*(1-alpha_bk)) * 255



    cv2.imshow('Webcam', newbkg) 
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff  
    if k==27:
        break
# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()