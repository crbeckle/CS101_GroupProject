from string import lower
import pyaudio  
import wave
import create
import time
import random
import math

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
	print "Welcome to SOMI Says!"
	r.turn(45,50)
	r.turn(-45,50)

def success():
	r.go(0,-20)
	r.playSong([(60,8),(64,8),(67,8),(72,16),(71,8),(72,16)])
	time.sleep(0.5)
	r.go(0,20)
	r.playSong([(60,8),(64,8),(67,8),(72,16),(71,8),(72,16)])
	time.sleep(0.5)
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
	response = ""
	while True:
		response = raw_input("Do you want to play again? ")
		if lower(response) not in ("y", "n", "yes", "no"):
			print "Please give an actual yes or no response."
			continue
		else:
			return lower(response) in ("y", "yes")

def func1():
	response = input("What is 2 + 2? ")
	if response == 4:
		return True
	else:
		return False
		
def func2():
	response = input("What is 3 + 2? ")
	if response == 5:
		return True
	else:
		return False
		
def func3():
	response = input("What is 4 * 2? ")
	if response == 8:
		return True
	else:
		return False
	
def bumpNoseFunc():
	print("Bump my nose!")
	timeout = 0
	while True:
		sensors = r.sensors([create.RIGHT_BUMP, create.LEFT_BUMP])
		if (sensors[create.RIGHT_BUMP] == 1 or sensors[create.LEFT_BUMP] == 1):
			return True
		time.sleep(0.5)
		timeout += 1
		if (timeout == 20):
			return False

def catchMe():
	#caution: this function has not been tested!
	time.sleep(4)
	#playMusic(hit_my_nose.avi)
	sensors = r.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
	end = False
	#set the point in time when somi says the player was too slow
	timeout = time.clock() + 4
	while(True):
		#move in reverse and pick a random turning speed to make it semi-difficult to catch
		r.go(-50,random()*90-45)
		#set a point in time when somi will alter its course
		tEnd = time.clock() + random()+.2
		while (time.clock() < tEnd):
			#until it is time to alter somi's course, check if 
			#the bumper has been hit (win condition) 
			if (sensors[create.LEFT_BUMP] == 1 or sensors[create.RIGHT_BUMP] == 1):
				return True
			#or if somni has timed out (lose condition)
			if (time.clock() > timeout):
				return False
								
def resetPosition()
	#Caution - not tested with Somni!
	#rotate to face toward the start position and then move foward until it is reached
	#this is so somi is less likely to drift into a corner of the room
	pose = r.getPose()
	direction = 360 * atan2(pose[1],pose[0])/(2*math.pi)+180
	r.turn(direction - pose[2],30)
	distance = math.sqrt(math.pow(pose[0],2) + math.pow(pose[1],2))
	r.move(distance,30)
								
def main():
	welcome()
	while True:
		shuffle(commands)
		for test in commands:
			if test():
				success()
			else:
				failure()
		if proceed():
			continue
		else:
			print("Goodbye!")
			break
	
r = create.Create(3)
commands = [bumpNoseFunc]
main()
