import pyaudio  
import wave
import create
import time
import random
import os
#import win32api
#import win32con
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

    PressKey(0x11) #CTRL
    PressKey(0x53) #S

    #optional : if you want to see the atl-tab overlay

    ReleaseKey(0x11) #~CTRL
    ReleaseKey(0x53) #~S

def clear():
    PressKey(0x11)
    PressKey(0x41)
    
   
    
    ReleaseKey(0x11)#ctrl
    ReleaseKey(0x41)#a
    
    PressKey(0x08)#backspace

def MicToggle():
    PressKey(0x11) #CTRL
    PressKey(0x31) #1
    ReleaseKey(0x11)
    ReleaseKey(0x31)

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
    time.sleep(5)
    print "Welcome to SOMI Says!"
    r.go(0,-60)
    time.sleep(0.3)
    r.go(0,60)
    time.sleep(0.6)
    r.go(0,-60)
    time.sleep(0.3)
    r.go(-20)
    time.sleep(0.4)
    r.go(20)
    time.sleep(0.4)
    r.stop()
    playMusic("C:\\Beckley\\Eclipse_Workspace\\CS101_SOMISays\\tada.wav")
    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_Intro.wav")

def success():
    successSoundFile = random.choice(["C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_SuccessHooray.wav"
                                      ,"C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_SuccessGoodJob.wav",
                                      "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_SuccessYouDidIt.wav"])
    r.go(-20)
    time.sleep(0.4)
    r.go(20)
    time.sleep(0.4)
    r.stop()
    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\Successful.wav")
    playMusic(successSoundFile)
    print "Success!"

def failure():
    r.go(0,-60)
    time.sleep(0.3)
    r.go(0,60)
    time.sleep(0.6)
    r.go(0,-60)
    time.sleep(0.3)
    r.stop()
    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\SOMISounds\\Nope.wav")
    if (failureTimeout == False):
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureGoodTry.wav")
    else:
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureTimeout.wav")
    print "Failure!"

def waiting():
    if (random.random() < 0.5):
        r.go(0,-25)
    else:
        r.go(0,25)
    print "I'm waiting"
    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_WaitingForInput.wav")
    r.stop()

def proceed():
    #SendInput = ctypes.windll.user32.SendInput
    path_to_file = "C:\\Beckley\\Eclipse_Workspace\\CS101_SOMISays\\playagain.txt"
    subprocess.Popen(["notepad.exe", path_to_file])
    time.sleep(1)
    clear()
    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_RepeatPlayMessage.wav")
    MicToggle()
    time.sleep(7)
    MicToggle()
    save()
    time.sleep(1)
    os.system("TASKKILL /F /IM notepad.exe")
    time.sleep(1)
    myfile = open(path_to_file)
    myfile.seek(0)
    line = myfile.readline()
    line = line.lower()
    if("yes" in line or "yeah" in line):
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_RepeatIsYES.wav")
        return True
    else:
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_Goodbye.wav")
        return False

def whatAnimalMakesThisNoise():
    #Choose a mode of play (and corresponding animal sound file) at random:
    #    Mode 0 = Dog
    #    Mode 1 = Horse
    #    Mode 2 = Tiger
    modeOfPlay = random.choice([0,1,2])
    animalSoundFile = ''
    if (modeOfPlay == 0):#Dog
        animalSoundFile = "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_AnimalSoundDog.wav"
    elif (modeOfPlay == 1):#Horse
        animalSoundFile = "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_AnimalSoundHorse.wav"
    else:#Tiger
        animalSoundFile = "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_AnimalSoundTiger.wav"
        
    #retryCount tracks the number of attempts (up to a maximum of three) and timeOut tracks whether or not the user has timed out.
    #After three tries, or if a time out occurs, the function will return False
    #Timing out uses the fact that checking for input is done in 5 second intervals. If 5 seconds pass with no input, the waiting function
    #    is called. If 10 seconds pass with no input, the user has timed out (regardless of which attempt they are on)
    retryCount = 0
    timeOut = 0
    path_to_file = "C:\\Beckley\\Eclipse_Workspace\\CS101_SOMISays\\guesstheanimal.txt"
    
    while (True):
        #Open a Notepad file for the voice recognition software to dictate to and clear its previous contents
        subprocess.Popen(["notepad.exe", path_to_file])
        time.sleep(1)
        clear()
        
        #Play the sound file to prompt user input
        playMusic(animalSoundFile)
        
        #Gather the user input over 5 seconds
        MicToggle()
        time.sleep(7)
        MicToggle()
        
        #Save the input and kill Notepad
        save()
        time.sleep(1)
        os.system("TASKKILL /F /IM notepad.exe")
        time.sleep(1)
        
        #Process the first line of the input. The possible conditions are:
        #    Empty: 
        #           if the timeOut variable has already been incremented (i.e. 10 seconds have passed), return False
        #           else, call the waiting function and increment the time out counter
        #    Non-Empty:
        #           if key words of the current mode of play animal are found in the first line, return True
        #           else, if this is the third attempt, return False, else play the correction sound file, increment the retry counter, and
        #           reset the time out counter
        myfile = open(path_to_file)
        myfile.seek(0)
        line = myfile.readline()
        line = line.lower()
        line = line.strip()
        if (line == ''):
            if (timeOut == 1):
                global failureTimeout
                failureTimeout = True
                return False
            else:
                waiting()
                timeOut += 1
        elif (modeOfPlay == 0):#Dog
            if(('dog' in line) or 
                ('doggy' in line)):
                return True
            else:
                if (retryCount == 2):
                    return False
                else:
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureWrongAnimal.wav")
                    retryCount += 1
                    timeOut = 0
        elif (modeOfPlay == 1):#Horse
            if(('horse' in line) or 
                ('horsey' in line)):
                return True
            else:
                if (retryCount == 2):
                    return False
                else:
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureWrongAnimal.wav")
                    retryCount += 1
                    timeOut = 0
        elif (modeOfPlay == 2):#Tiger
            if(('tiger' in line) or 
                ('lion' in line) or
                ('dinosaur' in line)):
                return True
            else:
                if (retryCount == 2):
                    return False
                else:
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureWrongAnimal.wav")
                    retryCount += 1
                    timeOut = 0
        
        if (line != ''):
            time.sleep(0.5)
            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureLetsTryAgain.wav")

def whatDoesThisAnimalSoundLike():
    #Choose a mode of play (and corresponding animal sound file) at random:
    #    Mode 0 = Cat
    #    Mode 1 = Cow
    #    Mode 2 = Sheep
    modeOfPlay = random.choice([0,1,2])
    animalSoundFile = ''
    if (modeOfPlay == 0):#Cat
        animalSoundFile = "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_WhatisCatSound.wav"
    elif (modeOfPlay == 1):#Cow
        animalSoundFile = "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_WhatisCowSound.wav"
    else:#Sheep
        animalSoundFile = "C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_WhatisSheepSound.wav"
        
    #retryCount tracks the number of attempts (up to a maximum of three) and timeOut tracks whether or not the user has timed out.
    #After three tries, or if a time out occurs, the function will return False
    #Timing out uses the fact that checking for input is done in 5 second intervals. If 5 seconds pass with no input, the waiting function
    #    is called. If 10 seconds pass with no input, the user has timed out (regardless of which attempt they are on)
    retryCount = 0
    timeOut = 0
    path_to_file = "C:\\Beckley\\Eclipse_Workspace\\CS101_SOMISays\\makeanimalsounds.txt"
    
    while (True):
        #Open a Notepad file for the voice recognition software to dictate to and clear its previous contents
        subprocess.Popen(["notepad.exe", path_to_file])
        time.sleep(1)
        clear()
        
        #Play the sound file to prompt user input
        playMusic(animalSoundFile)
        
        #Gather the user input over 5 seconds
        MicToggle()
        time.sleep(7)
        MicToggle()
        
        #Save the input and kill Notepad
        save()
        time.sleep(1)
        os.system("TASKKILL /F /IM notepad.exe")
        time.sleep(1)
        
        #Process the first line of the input. The possible conditions are:
        #    Empty: 
        #           if the timeOut variable has already been incremented (i.e. 10 seconds have passed), return False
        #           else, call the waiting function and increment the time out counter
        #    Non-Empty:
        #           if key words of the current mode of play animal are found in the first line, return True
        #           else, if this is the third attempt, return False, else play the correction sound file, increment the retry counter, and
        #           reset the time out counter
        myfile = open(path_to_file)
        myfile.seek(0)
        line = myfile.readline()
        line = line.lower()
        line = line.strip()
        if (line == ''):
            if (timeOut == 1):
                global failureTimeout
                failureTimeout = True
                return False
            else:
                waiting()
                timeOut += 1
        elif (modeOfPlay == 0):#Cat
            if(('meow' in line) or 
                ('now' in line) or
                ('me' in line)):
                return True
            else:
                if (retryCount == 2):
                    return False
                else:
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureNotCatSound.wav")
                    retryCount += 1
                    timeOut = 0
        elif (modeOfPlay == 1):#Cow
            if(('moo' in line) or 
                ('new' in line) or
                ('knew' in line)):
                return True
            else:
                if (retryCount == 2):
                    return False
                else:
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureNotCowSound.wav")
                    retryCount += 1
                    timeOut = 0
        elif (modeOfPlay == 2):#Sheep
            if(('baa' in line) or 
                ('bad' in line) or
                ('that' in line)):
                return True
            else:
                if (retryCount == 2):
                    return False
                else:
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureNotSheepSound.wav")
                    retryCount += 1
                    timeOut = 0
        
        if (line != ''):
            time.sleep(0.5)
            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureLetsTryAgain.wav")

def highFive():
    # left bumper is right hand and vice versa
    modeOfPlay = random.choice([0,1,2])
    if (modeOfPlay == 0):
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_LeftHighFive.wav")
    elif (modeOfPlay == 1):
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_RightHighFive.wav")
    else:
        playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_BumpMyNose.wav")
    #part = random.choice(["left hand","nose","right hand"])
    #print("Bump my %s!" % part)
    timeout = time.clock() + 10
    # until the timeout is reached, the program will check the sensors. If either is pressed,
    # triggered will become True and the program will check 0.2 seconds later to make sure
    # that the sensors are fully pressed (i.e. if I try to press the nose and the left hand
    # happens to get pressed a millisecond before the right hand does, it shouldn't matter)
    triggered = False
    tries_left = 3
    while True:
        if (time.clock() > timeout or tries_left == 0):
            if (time.clock() > timeout):
                global failureTimeout
                failureTimeout = True
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
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\highfive.wav")
                    pressed = 0 # Left Hand
                if (sensors[create.RIGHT_BUMP] == 0 and sensors[create.LEFT_BUMP] == 1):
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\highfive.wav")
                    pressed = 1 # Right Hand
                if (sensors[create.RIGHT_BUMP] == 1 and sensors[create.LEFT_BUMP] == 1):
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_BumperBoop.wav")
                    pressed = 2 # Nose
                
                if (modeOfPlay == pressed):
                    # Correct sensors pressed! Good job!
                    return True
                else:
                    # Wrong sensors pressed! Try again
                    #print("Sorry, that was my %s! Try again!" % pressed)
                    if (modeOfPlay == 0):
                        if (pressed == 1):
                            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureHitRightHand.wav")
                        else:
                            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureHitNose.wav")
                    elif (modeOfPlay == 1):
                        if (pressed == 0):
                            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureHitLeftHand.wav")
                        else:
                            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureHitNose.wav")
                    else:
                        if (pressed == 0):
                            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureHitLeftHand.wav")
                        else:
                            playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureHitRightHand.wav")
                    tries_left -= 1
                    time.sleep(0.5)
                    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_FailureLetsTryAgain.wav")
                    timeout = time.clock() + 10

def catchMe():
    playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_CatchMe.wav")
    time.sleep(2)
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
                playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_BumperBoop.wav")
                r.stop()
                counter += 1
                if (counter == 3):
                    # (win condition)
                    time.sleep(2)
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
                global failureTimeout
                failureTimeout = True
                return False

#def resetPosition():
#	#Caution - not tested with somi!
#	#rotate to face toward the start position and then move forward until it is reached
#	#this is so somi is less likely to drift into a corner of the room
#	pose = r.getPose()
#	direction = 360 * atan2(pose[1],pose[0])/(2*math.pi)+180
#	r.turn(direction - pose[2],30)
#	distance = math.sqrt(math.pow(pose[0],2) + math.pow(pose[1],2))
#	r.move(distance,30)

def main():
    welcome()
    while True:
        funcCount = 0
        random.shuffle(commands)
        for test in commands:
            global failureTimeout
            failureTimeout = False
            if (funcCount > 0 and funcCount < 4):
                playMusic("C:\\Users\\Chris\\Documents\\GitHub\\CS101_GroupProject\\soundsFixed\\SOMISays_NextQuestion.wav")
            if test():
                success()
            else:
                failure()
            funcCount += 1
            r.stop()
        if proceed():
            continue
        else:
            print("Goodbye!")
            break

r = create.Create(3)
commands = [whatDoesThisAnimalSoundLike]
failureTimeout = False
main()
