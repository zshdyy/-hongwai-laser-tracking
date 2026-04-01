import pigpio
import time
pi = pigpio.pi()
#GPIO.setmode(GPIO.BCM)
pi.set_servo_pulsewidth(23, 1500)
pi.set_servo_pulsewidth(24, 1500)
time.sleep(2)
pi.set_servo_pulsewidth(23, 2000)
pi.set_servo_pulsewidth(24, 1600)

