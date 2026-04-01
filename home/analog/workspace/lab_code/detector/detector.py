#!/usr/bin/env python3 
import cv2 as cv 
import numpy as np
#from transform import four_point_transform

def find_red_point_on_line(image, outline):
    left = min(outline[0][0], outline[2][0]) - 15
    right = max(outline[1][0], outline[3][0]) + 15
    top = min(outline[0][1], outline[1][1]) - 15
    bottom = max(outline[2][1], outline[3][1]) + 15
    reg = image[top:bottom, left:right]
    
    hsv = cv.cvtColor(reg, cv.COLOR_BGR2HSV)
    lower1 = np.array([0, 43, 45])
    upper1 = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, lower1, upper1)

    lower2 = np.array([156, 43, 45])
    upper2 = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower2, upper2)
    mask = mask1 + mask2
    
    red_pix = np.column_stack(np.where(mask > 100))
    #print(red_pix)
    if len(red_pix)== 0:
        print('found nothing on line')
        return None
    centroid = np.round(np.mean(red_pix, axis=0)).astype(int)
    #print(centroid)
    cv.circle(reg, (centroid[1], centroid[0]), 3, (255, 0, 0), 2)
    cv.imshow('cropped', reg)
    # cv.imshow('masked', mask)
    return (centroid[1] + left, centroid[0] + top)


def find_green_point_on_line(image, outline):
    left = min(outline[0][0], outline[2][0]) - 15
    right = max(outline[1][0], outline[3][0]) + 15
    top = min(outline[0][1], outline[1][1]) - 15
    bottom = max(outline[2][1], outline[3][1]) + 15
    reg = image[top:bottom, left:right]
    
    hsv = cv.cvtColor(reg, cv.COLOR_BGR2HSV)
    lower = np.array([35, 43, 46])
    upper = np.array([77, 255, 255])
    mask = cv.inRange(hsv, lower, upper)
    
    red_pix = np.column_stack(np.where(mask > 100))
    #print(red_pix)
    if len(red_pix)== 0:
        print('found nothing on line')
        return None
    centroid = np.round(np.mean(red_pix, axis=0)).astype(int)
    #print(centroid)
    cv.circle(reg, (centroid[1], centroid[0]), 3, (255, 0, 0), 2)
    cv.imshow('cropped', reg)
    # cv.imshow('masked', mask)
    return (centroid[1] + left, centroid[0] + top)

def red_point(image, outline):
    scale = 2
    image = cv.resize(image, (0, 0), fx = 1 / scale, fy = 1 / scale)
    outline = list(map(lambda o: (o / scale).astype(int), outline))
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower1 = np.array([0, 43, 100])
    upper1 = np.array([5, 255, 255])
    mask1 = cv.inRange(hsv, lower1, upper1)

    lower2 = np.array([156, 43, 100])
    upper2 = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower2, upper2)
    mask = mask1 + mask2

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    blurred = cv.blur(mask, (5, 5))
    #cv.imshow('blurred', blurred)
    conts, hierachy = cv.findContours(blurred, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    if len(conts) < 2: 
        print(f'warning: cannot find enough region ({len(conts)})')
        #try to find on the line
        ret = find_red_point_on_line(image, outline)
        if ret is None:
            return None
        cv.circle(image, ret, 3, (255, 0, 0), 2)
        cv.imshow('cont', image)
        cv.waitKey(1)
        return (ret[0] * scale, ret[1] * scale)
    if len(conts) > 2:
        print('warning: avoid other red objects in the scene')

    max_cont_index = 0
    max_area = cv.contourArea(conts[0])
    # print(len(conts), len(hierachy), hierachy.shape)
    for i in range(0, len(conts)):
        if cv.contourArea(conts[i]) > max_area:
            max_area = cv.contourArea(conts[i])
            max_cont_index = i

    child_index = hierachy[0][max_cont_index][2] # assume the red light have only one white hole

    # child_index != -1:
     #   child_index = hierachy[0][child_index][0]
      #  child.append(child_index)


    mo = cv.moments(conts[child_index])
    x, y = int(mo['m10'] / (mo['m00'] + 1e-5)), int(mo['m01'] / (mo['m00'] + 1e-5))
    
    cv.circle(image, (x, y), 3, (255, 0, 0), 2)
    cv.drawContours(image, conts, -1, (0, 255, 0), 3)
    cv.imshow('cont', image)
    cv.waitKey(1)
    #print(x, y)
    #point = np.dot(trans, np.array([[x * scale, y * scale, 1]], dtype = np.float32).T).T
    #print(point)
    return (x * scale, y * scale)

def green_point(image, outline):
    scale = 2
    image = cv.resize(image, (0, 0), fx=1 / scale, fy=1 / scale)
    outline = list(map(lambda o: (o / scale).astype(int), outline))
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower = np.array([35, 43, 46])
    upper = np.array([77, 255, 255])
    mask = cv.inRange(hsv, lower, upper)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    blurred = cv.blur(mask, (5, 5))

    conts, hierachy = cv.findContours(blurred, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    if len(conts) < 2: 
        print(f'warning: cannot find enough region ({len(conts)})')
        #try to find on the line
        ret = find_green_point_on_line(image, outline)
        if ret is None:
            return None
        cv.circle(image, ret, 3, (255, 0, 0), 2)
        cv.imshow('cont', image)
        cv.waitKey(1)
        return (ret[0] * scale, ret[1] * scale)
    if len(conts) > 2:
        print('warning: avoid other red objects in the scene')

    max_cont_index = 0
    max_area = cv.contourArea(conts[0])
    for i in range(0, len(conts)):
        if cv.contourArea(conts[i]) > max_area:
            max_area = cv.contourArea(conts[i])
            max_cont_index = i

    mo = cv.moments(conts[max_cont_index])
    x, y = int(mo['m10'] / (mo['m00'] + 1e-5)), int(mo['m01'] / (mo['m00'] + 1e-5))
    
    cv.circle(image, (x, y), 3, (255,  0, 0), 2)
    cv.drawContours(image, conts, -1, (255, 0, 0), 1)
    cv.imshow('cont', image)
    cv.waitKey(1)

    return (x * scale, y * scale)



## get the corner of a rectangle
def corner(image):
    img = image.copy()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    #cv.imshow('blurred', blurred)
    edges = cv.Canny(blurred, 0, 150, apertureSize = 5)
    close_kernel = cv.getStructuringElement(cv.MORPH_CROSS, (7, 7))
    edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, close_kernel)
    open_kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    edges = cv.morphologyEx(edges, cv.MORPH_OPEN, open_kernel)

    #cv.imshow('edge', edges)
    
    conts, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #epsilon = [0.02 * cv.arcLength(cont, True) for cont in contours]
    #approx = [cv.approxPolyDP(cont, eps, True) for (cont, eps) in zip(contours, epsilon)]
    #contours = filter(lambda apr: len(apr) == 4 and cv.contourArea(apr) > 1000, approx)

    max_cont = conts[0]
    bounding = cv.boundingRect(max_cont)
    max_bounding_size = bounding[2] * bounding[3]
    for i in conts:
        bounding = cv.boundingRect(i)
        if bounding[2] * bounding[3] > max_bounding_size:
            max_cont = i
            max_bounding_size = bounding[2] * bounding[3]

    cont_img = np.zeros((img.shape[0], img.shape[1], 1), dtype = np.uint8)
    cv.drawContours(cont_img, [max_cont], 0, 255, 5)

    conts, _ = cv.findContours(cont_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(conts) != 1:
        print("warning: more than one outer contour")

    cont_img = np.zeros(cont_img.shape, dtype = np.uint8)
    cv.drawContours(cont_img, conts, 0, 255, 25)

    #cv.drawContours(image, conts, -1, (0, 255, 0), 10)
    #cv.imshow('test', image)

    conts, hierarchy = cv.findContours(cont_img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    if len(hierarchy) != 1:
        print("warning: more than one outer contour in step 2")

    max_inner_contour = conts[0]
    max_inner_area = 0
    for (i, hiera) in zip(conts, hierarchy[0]):
        if(hiera[3] == -1):
            continue # skip, because it is the father!

        if cv.contourArea(i) > max_inner_area:
            max_inner_area = cv.contourArea(i)
            max_inner_contour = i

    cv.drawContours(img, [max_inner_contour], -1, (0, 255, 0), 1)
    cv.imshow('test2', img)

    cont = max_inner_contour
    dist = [(i[0][0] - 0)**2 + (i[0][1] - 0)**2 for i in cont]
    lt = cont[dist.index(min(dist))]
    dist = [(i[0][0] - image.shape[1])**2 + (i[0][1] - 0)**2 for i in cont]
    rt = cont[dist.index(min(dist))]
    dist = [(i[0][0] - 0)**2 + (i[0][1] - image.shape[1])**2 for i in cont]
    lb = cont[dist.index(min(dist))]
    dist = [(i[0][0] - image.shape[1])**2 + (i[0][1] - image.shape[1])**2 for i in cont]
    rb = cont[dist.index(min(dist))]
    return (lt[0], rt[0], lb[0], rb[0])
    #print((lt, rt, lb, rb))
    #self.T = four_point_transform([lt, rt, rb, lb])
    #warped = cv.warpPerspective(image, self.T, (100, 100))
    #cv.imshow('test', warped)
    
def rectangle(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT,  (9, 9))
    mopho = cv.erode(gray, kernel)
    _, mopho = cv.threshold(mopho, 0, 255, cv.THRESH_OTSU)
    #cv.imshow('mopho', mopho)
    conts, hier = cv.findContours(mopho, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    conts = [(conts[idx], conts[i[2]], i[2]) for (idx, i) in enumerate(hier[0]) if hier[0][i[2]][0] == -1 and i[2] != -1]
    #print(list(map(lambda c: c[2], conts)))
    #print(len(conts))
    if len(conts) == 0:
        print('not detected')
    if len(conts) > 1:
        print('more than one?')
        
    cont = conts[0]
    approx_out = cv.approxPolyDP(cont[0], 0.02 * cv.arcLength(cont[0], True), True)
    approx_inner = cv.approxPolyDP(cont[1], 0.02 * cv.arcLength(cont[1], True), True)
    approx_inner = np.concatenate(([approx_inner[0]], approx_inner[1:][::-1]))
    cv.drawContours(image, [approx_out], -1, (0, 255, 0), 5)
    cv.drawContours(image, [approx_inner], -1, (0, 255, 0), 5)
    
    #cv.drawContours(image, [], -1, (0, 255, 0), 5)
    cv.imshow('test', image)
    cv.waitKey(1)

    out_rate = 0.6
    pts = np.round(out_rate * approx_out + (1 - out_rate) * approx_inner).astype(int)
    for p in pts:
        cv.circle(image, p[0], 3,(0, 255, 0), 5)
    cv.imshow('rect', image)
    #print(pts)
    
    src_pts = np.float32(list(map(lambda p: p[0], pts)))
    dst_pts = np.float32([[210, 0], [210, 297], [0, 297], [0, 0]])
    
    M = cv.getPerspectiveTransform(src_pts, dst_pts)
    #warpped = cv.warpPerspective(image, M, (210, 297))
    #cv.imshow('warpped', warpped)
    return src_pts, M
    
    #TODO: bount with        
#

def test2():
    from camera import Camera
    cam = Camera()
    img = cam.get_image()
    outline = corner(img)
    while True:
        img = cam.get_image()
        #print(outline)
        green_point(img, outline)
        if cv.waitKey(2) == ord('q'):
            break
        
#from camera import Camera
def test1():
    from camera import Camera
    cam = Camera()
    while True:
        img = cam.get_image()
        rectangle(img)
        #conts = det.corner(img)
   
if __name__ == '__main__':
    test2()
