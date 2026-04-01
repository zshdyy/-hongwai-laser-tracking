
import pigpio
import time
from detector.detector import corner
from detector.detector import rectangle
from detector.detector import red_point
from detector.camera import Camera
import cv2 as cv
import numpy as np

pi = pigpio.pi()
yaw = 23
pitch = 24


global Yaw, Pitch
global Mx,My
global LT,RT,RB,LB
global LT_x, LT_y,RT_x, RT_y,RB_x, RB_y,LB_x, LB_y
global current_yaw,current_pitch
global outline
global Trans, Trans_Inv

cam = Camera()


def set_servo_angle(servo, angle):
    pi.set_servo_pulsewidth(servo,500.0 + 2000.0 / 180.0 * (1.0 * angle))

def Get_Big():
    global outline
    image1 = cam.get_image()
    outline = corner(image1)
    
def Get_point():
    global LT_x, LT_y,RT_x, RT_y,RB_x, RB_y,LB_x, LB_y, Trans, Trans_Inv
    image0 = cam.get_image()
    (LT,RT,RB,LB), Trans = rectangle(image0)
    LT_x, LT_y = LT[0], LT[1]
    RT_x, RT_y = RT[0], RT[1]  
    RB_x, RB_y = RB[0], RB[1]  
    LB_x, LB_y = LB[0], LB[1] 
    _, Trans_Inv = cv.invert(Trans)

def Get_MyPos():
    global outline, Mx,My
    
    #point = None
    #while point is None:
    img = cam.get_image()
    point = red_point(img, outline)
    #    print('not detect red point')
    #print(f'detected red point: {point}')
    (Mx,My) = point
    

def move_to_target(target_x, target_y):
    Get_MyPos()  
    global Mx, My, Trans, Trans_Inv
    global current_yaw,current_pitch 
    
    error_x = target_x - Mx
    error_y = target_y - My
    last_yaw_angle = current_yaw
    last_pitch_angle  = current_pitch
    yaw_angle = current_yaw
    pitch_angle = current_pitch
    current_errorx = error_x
    current_errory = error_y
    last_errorx = 0.0
    last_errory = 0.0
    dt = 0.02
    while True:  
        Get_MyPos()  
        error_x = target_x - Mx
        error_y = target_y - My
        if abs(error_x) < 5 and abs(error_y) < 5: 
            break
        #recall_x = 0
        #recall_y = 0
        #if horizontal is not None :
         #   recall = cv.perspectiveTransform(np.array([[[error_x, error_y]]], dtype = np.float32), Trans)
          #  recall = recall[0][0]
           # normal_axis = []
            #if horizontal is True:
             #   normal_axis = [recall[0], 0]
            #elif horizontal is False:
                #normal_axis = [0, recall[1]]
            #print(error_x, error_y)
            #print(f'normal_axis: {normal_axis}')
            #try:normal_axis
            #print(f'trans: {Trans}')
            #print(f'trans_inv: {Trans_Inv}')
            #recall = cv.perspectiveTransform(np.array([[normal_axis]], dtype = np.float32), Trans_Inv)
            #except:
                #print('failed to calculae recall')
                #recall = [[[0, 0]]]
            #recall = recall[0][0]
            #recall_x = recall[0]
            #recall_y = recall[1]
            
        #error_x = error_x + 0.0 * recall_x
        #error_y = error_y + 0.0 * recall_y
            
        #print(f'recall x: {recall_x}, y: {recall_y}')
        last_yaw_angle = yaw_angle
        last_pitch_angle = pitch_angle
        yaw_angle = limit_number(last_yaw_angle + error_x/1000 +0.000*(current_errorx-last_errorx),last_yaw_angle - 0.6, last_yaw_angle + 0.6)
        pitch_angle = limit_number(last_pitch_angle + error_y/1000 -0.000*(current_errory-last_errory), last_pitch_angle-0.6, last_pitch_angle +0.6)
        print(f"angle is {yaw_angle} {pitch_angle}")
        current_yaw = yaw_angle
        current_pitch = pitch_angle
        last_errorx = current_errorx
        last_errory = current_errory
        if(yaw_angle > pitch_angle):
            set_servo_angle(yaw, yaw_angle)
            set_servo_angle(pitch, pitch_angle)
        else:
            set_servo_angle(pitch, pitch_angle)
            set_servo_angle(yaw, yaw_angle)

        #print(f"errorx is {error_x} {error_y}")
        #print(f"Mx is {Mx} {My}")
        #print(f"target is {target_x} {target_y}")
        #print(f" rrrr is {current_yaw-last_yaw_angle} {current_pitch-last_pitch_angle}")     
        
        time.sleep(dt)  
        
    
    
def limit_number(number, min_value, max_value):
    if number < min_value:
        number = min_value
    if number > max_value:
        number = max_value
    return number
    
def reset():
    global current_yaw,current_pitch
    current_yaw = 89
    current_pitch  = 92
    set_servo_angle(pitch, current_pitch)
    set_servo_angle(yaw, current_yaw)
 

def big():
    global current_yaw,current_pitch
    set_servo_angle(pitch, 100.5)
    time.sleep(1)
    set_servo_angle(yaw, 80)
    time.sleep(1)
    set_servo_angle(pitch, 83)
    time.sleep(2)
    set_servo_angle(yaw, 99)
    time.sleep(2)
    set_servo_angle(pitch, 100.5)
    time.sleep(2)
    set_servo_angle(yaw, 89)
    time.sleep(1)
    current_yaw = 89
    current_pitch  = 100.5
    
    
    

def small():
    global current_yaw,current_pitch 
    Get_point()
    global LT_x, LT_y,RT_x, RT_y,RB_x, RB_y,LB_x, LB_y
    move_to_target(RB_x,RB_y)
    yaw1 = current_yaw
    pitch1 = current_pitch
    time.sleep(1)
    #move_to_target(0.33*LB_x+0.67*RB_x,0.33*LB_y+0.67*RB_y)
    move_to_target(0.5*(LB_x+RB_x),0.5*(LB_y+RB_y))
    #move_to_target(0.67*LB_x+0.33*RB_x,0.67*LB_y+0.33*RB_y)
    move_to_target(LB_x,LB_y)
    yaw2 = current_yaw
    pitch2 = current_pitch
    time.sleep(1)
    #move_to_target(0.25*LT_x+0.75*LB_x,0.25*LT_y+0.75*LB_y)
    move_to_target(0.5*(LT_x+LB_x),0.5*(LT_y+LB_y))
    #move_to_target(0.75*LT_x+0.25*LB_x,0.75*LT_y+0.25*LB_y)
    move_to_target(LT_x,LT_y)
    yaw3 = current_yaw
    pitch3 = current_pitch
    time.sleep(1)
    #move_to_target(0.33*RT_x+0.67*LT_x,0.33*RT_y+0.67*LT_y)
    #move_to_target(0.5*RT_x+0.5*LT_x,0.5*RT_y+0.5*LT_y)
    #move_to_target(0.67*RT_x+0.33*LT_x,0.67*RT_y+0.33*LT_y)
    #move_to_target(RT_x,RT_y)
    current_yaw -= yaw2-yaw1
    current_pitch -=pitch2-pitch1 
    set_servo_angle(yaw,current_yaw)
    set_servo_angle(pitch,current_pitch)
    time.sleep(1)
    #move_to_target(0.25*RB_x+0.75*RT_x,0.25*RB_y+0.75*RT_y)
    #move_to_target(0.5*RB_x+0.5*RT_x,0.5*RB_y+0.5*RT_y)
    #move_to_target(0.75*RB_x+0.25*RT_x,0.75*RB_y+0.25*RT_y)
    #move_to_target(RB_x,RB_y)
    current_yaw += yaw2-yaw3
    current_pitch += pitch2-pitch3 
    set_servo_angle(yaw,current_yaw)
    set_servo_angle(pitch,current_pitch)
    time.sleep(1)
    
def main():
    try:
        Get_Big()
        Get_point()
        while True:
            mode = input('enter a mode: ')
            if mode == '1':
                reset()
                
            elif mode == '2':
                big()
            elif mode == '3':
                small()
            else:
                break
    except KeyboardInterrupt:
        pi.stop()

if __name__ == '__main__':
    main()

# Uncomment these lines if needed for manual control:
# gpio.output(pitch, gpio.HIGH)
# time.sleep(1e-6 * 1500.0) 
# gpio.output(pitch, gpio.LOW)
# gpio.output(yaw, gpio.HIGH)
# time.sleep(1e-6 * 1500.0) 
# gpio.output(yaw, gpio.LOW)
# gpio.cleanup()
