import cv2 as cv
idx = 0
cam = cv.VideoCapture(0)
while True:
    ret, img = cam.read()
    cv.imshow('disp', img)
    key = cv.waitKey(10)
    if key == ord('q'):
        break
    if key == ord('s'):
        cv.imwrite(f'img/{idx}.png', img)
        print(f'{idx} image')
        idx = idx + 1
