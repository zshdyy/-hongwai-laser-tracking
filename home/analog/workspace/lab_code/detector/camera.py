#!/usr/bin/env python3
import cv2 as cv
import numpy as np
class Camera():
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.map = None
        self.mtx = np.array([
        [907.59214944,   0.        , 670.28657045],
        [  0.        , 909.44702711, 371.08443633],
        [  0.        ,   0.        ,   1.        ]]
        #[911.96336073,   0.        , 649.87602282],
        #[  0.        , 908.41883644, 386.58558894],
        #[  0.        ,   0.        ,   1.        ]]
        , dtype = np.float32)
        self.dist = np.array([[-0.47747439,  0.12121833, -0.00313772,  0.0005717,   0.41171761]], dtype = np.float32)
        #self.dist = np.array([[-0.48869604,  0.3466519,   0.00467663, -0.00255965, -0.16493041]], dtype = np.float32)
    def get_image(self):
        ret, frame = self.cap.read()
        if self.map is None:
            h, w = frame.shape[:2]
            new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))
            self.map = cv.initUndistortRectifyMap(self.mtx, self.dist, None, new_camera_matrix, (w, h), 5)
        frame = cv.remap(frame, self.map[0], self.map[1], cv.INTER_LINEAR)
        if not ret:
            raise Exception('failed to read image')
         
        return frame

if __name__ == '__main__':
    cam = Camera()
    while(True):
        cv_img = cam.get_image()
        cv2.imshow('monitor', cv_img)
        key = cv2.waitKey(2)
        if key == ord('q'):
            break
