import time
import create
import random
r = create.Create(3)
time.sleep(4)
#playMusic(hit_my_nose.avi)
sensors = r.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
end = False
timeout = time.clock() + 4
while(True):
        r.go(-50,random()*90-45)
        tEnd = time.clock() + random()+.2
        while (time.clock() < tEnd):
                if (sensors[create.LEFT_BUMP] == 0 and sensors[create.RIGHT_BUMP] == 0):
                        exit(0)
                        #return True
                if (time.clock() > timeout):
                        exit(0)
                        #return False
