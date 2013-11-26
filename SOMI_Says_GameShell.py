from string import lower
import pyaudio  
import wave
import create
import time
import random
import math
import os
import win32api
import win32con
import ctypes
from dragonfly.all import *
import subprocess

##########################################################################################
#From Erik's code to get voice recognition working
#this is being used to save a file
SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
	_fields_ = [("wVk", ctypes.c_ushort),
				("wScan", ctypes.c_ushort),
				("dwFlags", ctypes.c_ulong),
				("time", ctypes.c_ulong),
				("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
	_fields_ = [("uMsg", ctypes.c_ulong),
				("wParamL", ctypes.c_short),
				("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
	_fields_ = [("dx", ctypes.c_long),
				("dy", ctypes.c_long),
				("mouseData", ctypes.c_ulong),
				("dwFlags", ctypes.c_ulong),
				("time",ctypes.c_ulong),
				("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
	_fields_ = [("ki", KeyBdInput),
				 ("mi", MouseInput),
				 ("hi", HardwareInput)]

class Input(ctypes.Structure):
	_fields_ = [("type", ctypes.c_ulong),
				("ii", Input_I)]

def PressKey(hexKeyCode):

	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
	x = Input( ctypes.c_ulong(1), ii_ )
	ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):

	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
	x = Input( ctypes.c_ulong(1), ii_ )
	ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
	
def save():

	PressKey(0x11) #Alt
	PressKey(0x53) #Tab

	#optional : if you want to see the atl-tab overlay

	ReleaseKey(0x11) #~Tab
	ReleaseKey(0x53) #~Alt

def clear():
	PressKey(0x11)
	PressKey(0x41)
	
   
	
	ReleaseKey(0x11)#ctrl
	ReleaseKey(0x41)#a
	
	PressKey(0x08)#backspace

def MicOn():
	PressKey(0x24)
	ReleaseKey(0x24)

#############################################################################################

def playMusic(mus_str):
	#define stream chunk   
	chunk = 1024  
	
	#open a wav format music  
	#f = wave.open(r"tada.wav","rb")
	f = wave.open(mus_str,"rb")
	
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)  
	#read data  
	data = f.readframes(chunk)  
	
	#play stream  
	while data != '':  
		stream.write(data)  
		data = f.readframes(chunk)  
	
	#stop stream  
	stream.stop_stream()  
	stream.close()  
	
	#close PyAudio  
	p.terminate()

def welcome():
	os.chdir(r"C:\Program Files (x86)\Nuance\NaturallySpeaking12\Program")
	os.startfile("natspeak.exe")
	time.sleep(35)
	MicOn()
	print "Welcome to SOMI Says!"
	r.turn(45,100)
	time.sleep(0.2)
	r.turn(-45,100)

def success():
	r.go(0,-30)
	#r.playSong([(60,8),(64,8),(67,8),(72,16),(71,8),(72,16)])
	time.sleep(0.3)
	r.go(0,30)
	#r.playSong([(60,8),(64,8),(67,8),(72,16),(71,8),(72,16)])
	time.sleep(0.3)
	playMusic("tada.wav")
	print "Congratulations, you're not an idiot!"

def failure():
	playMusic("EpicFailVoice.wav")
	print "You have displeased the machine spirit and forfeited your immortal soul to the darkness!"

def waiting():
	r.go(0,-20)
	print "I'm waiting"
	r.playSong([(67,16),(72,16),(67,16),(60,16),(67,16),(72,16),(67,16)])

def proceed():
	SendInput = ctypes.windll.user32.SendInput
	path_to_file = "playagain.txt"
	subprocess.Popen(["notepad.exe", path_to_file])
	time.sleep(1)
	clear()
	print("Do you want to play again? ")
	time.sleep(10)
	save()
	time.sleep(1)
	os.system("TASKKILL /F /IM notepad.exe")
	time.sleep(1)
	file = open(path_to_file)
	for line in file:
		return (line=="yes" or line=="Yes")
	#OLD VERSION
	#response = ""
	#while True:
	#	response = raw_input("Do you want to play again? ")
	#	if lower(response) not in ("y", "n", "yes", "no"):
	#		print "Please give an actual yes or no response."
	#		continue
	#	else:
	#		return lower(response) in ("y", "yes")

def whatAnimalMakesThisNoise():
	path_to_file = "guesstheanimal.txt"
	subprocess.Popen(["notepad.exe", path_to_file])
	time.sleep(1)
	clear()
	time.sleep(10)
	save()
	time.sleep(1)
	os.system("TASKKILL /F /IM notepad.exe")
	time.sleep(1)
	file = open(path_to_file)
	for line in file:
		if(line=="4"):
			return True
		if(line=="for"):
			return True
		if(line=="four"):
			return True
		if(line=="Four"):
			return True
		if(line=="For"):
			return True
		else:
			return False

def whatDoesThisAnimalSoundLike():
	path_to_file = "makeanimalsounds.txt"
	subprocess.Popen(["notepad.exe", path_to_file])
	time.sleep(1)
	clear()
	time.sleep(10)
	save()
	time.sleep(1)
	os.system("TASKKILL /F /IM notepad.exe")
	time.sleep(1)
	file = open(path_to_file)
	for line in file:
		if(line=="4"):
			return True
		if(line=="for"):
			return True
		if(line=="four"):
			return True
		if(line=="Four"):
			return True
		if(line=="For"):
			return True
		else:
			return False

	
def highFive():
	# left bumper is right hand and vice versa
	part = random.choice(["left hand","nose","right hand"])
	print("Bump my %s!" % part)
	timeout = time.clock() + 10
	# until the timeout is reached, the program will check the sensors. If either is pressed,
	# triggered will become True and the program will check 0.2 seconds later to make sure
	# that the sensors are fully pressed (i.e. if I try to press the nose and the left hand
	# happens to get pressed a millisecond before the right hand does, it shouldn't matter)
	triggered = False
	tries_left = 3
	while True:
		if (time.clock() > timeout or tries_left == 0):
			return False
		sensors = r.sensors([create.RIGHT_BUMP, create.LEFT_BUMP])
		if (not triggered):
			if (sensors[create.RIGHT_BUMP] == 1 or sensors[create.LEFT_BUMP] == 1):
				# Sensors triggered - give the user 0.2 seconds to finish pressing down, then check again.
				triggered = True
				time.sleep(0.2)
			else:
				# Nothing happened - wait 10 milliseconds then check again.
				time.sleep(0.01)
		else:
			if (not sensors[create.RIGHT_BUMP] == 1 and not sensors[create.LEFT_BUMP] == 1):
				# Sensors were triggered 0.2 seconds ago but no longer register, must've been a fluke
				triggered = False	
			else:
				pressed = ""
				if (sensors[create.RIGHT_BUMP] == 1 and sensors[create.LEFT_BUMP] == 0):
					pressed = "left hand"
				if (sensors[create.RIGHT_BUMP] == 0 and sensors[create.LEFT_BUMP] == 1):
					pressed = "right hand"
				if (sensors[create.RIGHT_BUMP] == 1 and sensors[create.LEFT_BUMP] == 1):
					pressed = "nose"
				
				if (part == pressed):
					# Correct sensors pressed! Good job!
					return True
				else:
					# Wrong sensors pressed! Try again
					print("Sorry, that was my %s! Try again!" % pressed)
					tries_left -= 1
					time.sleep(0.5)
					timeout = time.clock() + 10

def catchMe():
	time.sleep(2)
	#playMusic(hit_my_nose.avi)
	#set the point in time when somi says the player was too slow
	counter = 0
	timeout = time.clock() + 6
	while (True):
		#move in reverse and pick a random turning speed to make it semi-difficult to catch
		r.go(-50 + random.random() * random.random() * 20,random.random()*180-90)
		#set a point in time when somi will alter its course
		tEnd = time.clock() + random.random() / 2 + .2
		while (time.clock() < tEnd):
			r.getPose() # Piazza recommends doing this often to keep information up to date
			#until it is time to alter somi's course, check if 
			#the bumper has been hit (increment counter) 
			sensors = r.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
			if (sensors[create.LEFT_BUMP] == 1 or sensors[create.RIGHT_BUMP] == 1):
				r.stop()
				counter += 1
				if (counter == 3):
					# (win condition)
					time.sleep(2)
					#resetPosition()
					#time.sleep(2)
					return True
				else:
					# turn randomly, pause, and shoot off in a different direction with a new timer
					if (random.random() < 0.5):
						r.turn(int(random.random() * 180) , 40)
					else:
						r.turn(-int(random.random() * 180) , -40)
					time.sleep(2)
					timeout = time.clock() + 6
			#or if somi has timed out (lose condition)
			if (time.clock() > timeout):
				r.stop()
				time.sleep(2)
				#resetPosition()
				#time.sleep(2)
				return False
								
def resetPosition():
	#Note: pose data is extremely unreliable! Do not trust!
	#rotate to face toward the start position and then move forward until it is reached
	#this is so somi is less likely to drift into a corner of the room
	pose = r.getPose()
	print pose
	direction = 360 * math.atan2(pose[1],pose[0])/(2*math.pi)+180
	r.turn(int(direction - pose[2]) % 360, 30)
	distance = math.sqrt(math.pow(pose[0],2) + math.pow(pose[1],2))
	r.move(int(distance),30)
								
def main():
	welcome()
	while True:
		random.shuffle(commands)
		for test in commands:
			if test():
				success()
			else:
				failure()
			r.stop()
		if proceed():
			continue
		else:
			print("Goodbye!")
			break
	
r = create.Create(3)
commands = [highFive]
main()
