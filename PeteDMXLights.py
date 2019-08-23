import RPi.GPIO as GPIO
from pyudmx import pyudmx
import time

state = 0
dev = pyudmx.uDMXDevice()
dev.open()

def send_all_fade(dev, speed):
	cv = [0 for v in range(0, 512)]
	for x in range(0,31):
		cv[5+(x*8)] = 128
		cv[6+(x*8)] = 255
		cv[4+(x*8)] = speed
	try:
		sent = dev.send_multi_value(1, cv)
	except:
		dev = pyudmx.uDMXDevice()
		dev.open()

def send_all_color(dev,r,g,b,bright):
	cv = [0 for v in range(0, 512)]
	for x in range(0,31):
		cv[0+(x*8)] = r
		cv[1+(x*8)] = g
		cv[2+(x*8)] = b
		cv[6+(x*8)] = bright
	try:
		sent = dev.send_multi_value(1, cv)
	except:
		dev = pyudmx.uDMXDevice()
		dev.open()

def send_all_off(dev):
	cv = [0 for v in range(0, 512)]
	try:
		sent = dev.send_multi_value(1, cv)
	except:
		dev = pyudmx.uDMXDevice()
		dev.open()

def red_on(channel):
	global dev
	send_all_color(dev,255,0,0,255)

def fast(a):
	global dev
	global state
	state = 1
	send_all_fade(dev,255)

def slow(a):
	global state
	global dev
	print 'slow' + str(state)
	if state == 1:
		state = 0
		send_all_fade(dev,100)
	if state == 0:
		state = 1
		send_all_fade(dev,255)

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#GPIO.add_event_detect(13, GPIO.BOTH, callback=red_on)
	#GPIO.add_event_detect(21, GPIO.RISING, callback=fast)
        #GPIO.add_event_detect(13, GPIO.FALLING, callback=red_off)
        #GPIO.add_event_detect(21, GPIO.FALLING, callback=slow)
	send_all_fade(dev,100)
	fast = False
	red = False
	speed = False
	while True:
		if GPIO.input(13) != red:
			red = GPIO.input(13)
			if GPIO.input(13) == 1:
				red = GPIO.input(13)
				send_all_off(dev)
				send_all_color(dev,255,0,0,255)
			else:
				if fast:
					#fast = False
					send_all_fade(dev,255)
				else:
					#fast = True
					send_all_fade(dev,100)  
		if GPIO.input(21) != speed:
			speed = GPIO.input(21)
			if fast:
				fast = False
				send_all_fade(dev,100)
			else:
				fast = True
				send_all_fade(dev,255)	


		#send_all_fade(dev,255)
#		time.sleep(10)
		#send_all_fade(dev,100)
#		time.sleep(10)
		#send_all_color(dev,255,0,0,255)
		time.sleep(0.1)
	dev.close()


if __name__ == "__main__":
    main()
    print("Done")
