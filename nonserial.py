#dudewheresmypi
#ssh guest@192.168.1.153
#guest
#sftp://192.168.1.153/home/guest

import sys
import time
import random
import RPi.GPIO as GPIO		#import modules
import smbus
from serial import Serial
import constants

black = "\033[40m \033[0m"
red = "\033[41m \033[0m"
green = "\033[42m \033[0m"
yellow = "\033[43m \033[0m"
blue = "\033[44m \033[0m"
purple = "\033[45m \033[0m"
cyan = "\033[46m \033[0m"
white = "\033[47m \033[0m"   #list of colours with corresponding ANSI code

u = " \033[1D\033[1A"  #cursor up
d = " \033[1D\033[1B"  #cursor down
r = " \033[1D\033[1C"  #cursor right
l = " \033[1D\033[1D"  #cursor left

sleepTime = constants.sleepTime
initialSize = constants.initialSize	#constants from constants.py
upgradeTime = constants.upgradeTime


light = [5,6,12,13,16,19,20,26,26]	#ports in sequence for on board LEDs

i2cAddress = 0x38
bus = smbus.SMBus(1)	#initialising I2C for breadboard LEDs

serialPort = Serial("/dev/ttyAMA0", 11520)	#Initialising serial connection

def output(data):
        #serialPort.write(data)
	sys.stdout.write("\x1B[?25l")	#Output through serial connection
	sys.stdout.write(data)
	

def s1_superpad():
	GPIO.setmode(GPIO.BCM)	#
	global s1input_pin
	s1input_pin = 4
	GPIO.setup(s1input_pin,GPIO.IN,pull_up_down = GPIO.PUD_UP)
	if (upgrade1.isActive == False) and (paddle1.canUpgrade) and not(GPIO.input(s1input_pin)):
                paddle1.size = 5
                upgrade1.isActive = True
                upgrade1.count += 1 
                if upgrade1.count == 2:
                   paddle1.canUpgrade = False
	GPIO.cleanup()
	
def s1_serve():
	GPIO.setmode(GPIO.BCM)
	global s1input_pin2
	s1input_pin2 = 18
	GPIO.setup(s1input_pin2, GPIO.IN,pull_up_down = GPIO.PUD_UP)
	#GPIO.add_event_detect(s1input_pin2,GPIO.FALLING,bouncetime = 100)
	if not(GPIO.input(s1input_pin2)) and (game < 6) and not (ball.inPlay):
                ball.horz = 1
                ball.vert = 0
                ball.inPlay = True
	GPIO.cleanup()
	

def s2_superpad():
	GPIO.setmode(GPIO.BCM)
	global s2input_pin
	s2input_pin = 10
	GPIO.setup(s2input_pin, GPIO.IN,pull_up_down = GPIO.PUD_UP)
	#GPIO.add_event_detect(s2input_pin,GPIO.FALLING,bouncetime = 100)
	if (upgrade2.isActive == False) and (paddle2.canUpgrade) and not(GPIO.input(s2input_pin)):
                paddle2.size = 5
                upgrade2.isActive = True
                upgrade2.count += 1
                if upgrade2.count == 2:
                        paddle2.canUpgrade = False
	GPIO.cleanup()

def s2_serve():
	GPIO.setmode(GPIO.BCM)
	global s2input_pin2
	s2input_pin2 = 9
	GPIO.setup(s2input_pin2, GPIO.IN,pull_up_down = GPIO.PUD_UP)
	if (GPIO.input(s2input_pin2)) and (game > 5) and not (ball.inPlay):
                ball.horz = -1
                ball.vert = 0
                ball.inPlay = True
	GPIO.cleanup()



	


	

	


def select(x, y):		#move cursor to specified coordinates on screen
	sys.stdout.write("\033[" + str(y) + ";" + str(x) + "f")	



class Ball:

        inPlay = False

        def __init__(self, x, y):       #initialise variables
		self.x = x
		self.y = y
		self.horz = 1
		self.vert = 1
		self.speed = 1
		
	def draw(self, colour):         #draw with provided colour
		select(self.x, self.y)
		output(colour)

	def update(self):
                if self.inPlay:
			


			#bus.write_byte(i2cAddress, 0x01)#2**(self.x // 10))
			
                        if (self.y == 1) or (self.y == 24):     #bounce off top/bottom
                                self.vert *= -1			
                        self.x += self.horz
                        self.y += self.vert

			#time.sleep(0.1)



			#bus.write_byte(i2cAddress, 0xFF)#2**(self.x // 10))
                else:
                        if game < 6:
                                self.x = paddle1.x + 1
                                self.y = paddle1.y
                        else:
                                self.x = paddle2.x - 1
                                self.y = paddle2.y

	def bounce(self, pad):       #change direction
		self.horz *= -1
		self.speed = random.randint(1,3)
		if pad.y > self.y:
                        self.vert = -1
                if pad.y == self.y:
                        self.vert = 0
                if pad.y < self.y:
                        self.vert = 1

	def hits(self, pad):    #checks if ball is touching a paddle
		for i in range(-pad.size/2+1,pad.size/2+1):
			if (self.x + self.horz == pad.x) and (self.y == pad.y + i):
				return True
		return False

class Paddle:
		
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.size = initialSize
		self.canUpgrade = True
		self.vert = 1

	def draw(self, colour):
		for i in range(-self.size/2+1,self.size/2+1):
			select(self.x, self.y + i)
			output(colour)

	def update(self):
		if (constants.paddlesMoving):
			self.y += self.vert

	def atEdge(self):
		return (self.y == 1 + self.size/2) or (self.y == 24 - self.size/2)

class Score:
        txt = []

        txt.append(d + d + d + d + l + l + u + u + u + u + r + r)
	txt.append(l + r + d + d + d + d + d)
	txt.append(l + l + r + r + d + d + l + l + d + d + r + r + r)
	txt.append(l + l + r + r + d + d + l + r + d + d + l + l + l)
	txt.append(d + d + d + d + u + u + l + l + u + u + u)
	txt.append(l + l + d + d + r + r + d + d + l + l + l)
	txt.append(l + l + d + d + d + d + r + r + u + u + l + l)
	txt.append(l + l + r + r + d + d + d + d + d)
	txt.append(d + d + d + d + l + l + u + u + r + l + u + u + r + r)
        txt.append(l + l + d + d + r + r + u + d + d + d + l + l + l)
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.val = 0
		
        def draw(self, colour):
                select(self.x,self.y)
                #sys.stdout.write(colour[:10]+ self.txt[self.val] + colour[11:])
		output(colour[:5] +  self.txt[self.val] + "\033[0m")

class Upgrade:
        
	def __init__(self):
		self.time = 0
		self.isActive = False
		self.count = 0
		
        def update(self):
                if isActive:
                        self.time += 0.1


for i in range(1,81):
	for j in range(1,25):
		select(i,j)
		output("\033[40m \033[0m")
for i in range(1,25):
        if i % 3 != 0:
                select(40,i)
                output(green)

running = True
ball = Ball(40,12)
paddle1 = Paddle(3,constants.pad1_start)
paddle2 = Paddle(78,constants.pad2_start)
score1 = Score(31,2)
score2 = Score(51,2)
upgrade1 = Upgrade()
upgrade2 = Upgrade()
game = 1
frame = 1

score1.val = constants.player_1_score
score2.val = constants.player_2_score
score1.draw(red)
score2.draw(red)


while (running):

        if (ball.x == 39) or (ball.x == 41):
                for i in range(1,25):
                        if i % 3 != 0:
                                select(40,i)
                                output(green)                                
        	
	if (27 < ball.x < 33) and (ball.y < 7): 
		score1.draw(red)
	if (ball.y < 7) and (47 < ball.x < 53):
        	score2.draw(red)
	ball.draw(cyan)
	paddle1.draw(purple)    #Draw objects
	paddle2.draw(purple)  

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	pin = light[ball.x // 10]
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, True)
			

	time.sleep(sleepTime)
        if upgrade1.isActive:
                upgrade1.time += 1
        if upgrade2.isActive:           ###############Increase TIME##############
                upgrade2.time += 1

	GPIO.output(pin, False)#light[self.x // 10]
	GPIO.cleanup()

        if frame % ball.speed == 0:
                if (ball.x > 80):
                        if score1.val == 9:
                                running = False
                                break
                        score1.draw(black)
                        score1.val += 1
                        game += 1

                        if game > 10:
                                game = 1
                        score1.draw(red)        #Player 1 Scores
                        ball.inPlay = False

                        
                if (ball.x < 1):
                        if score2.val == 9:
                                running = False
                                break
                        score2.draw(black)
                        score2.val += 1
                        game += 1

                        if game > 10:
                                game = 1
                        score2.draw(red)         #Player 2 Scores
                        ball.inPlay = False



        if ball.hits(paddle1):
                ball.bounce(paddle1)
                frame = 0
        if ball.hits(paddle2):  #Ball bounces of paddles
                ball.bounce(paddle2)
                frame = 0

	paddle1.draw(black)     #undraw paddles
	paddle2.draw(black)


	paddle1.update()        #update positions
	paddle2.update()
	
        if frame % ball.speed == 0:
                
		ball.draw(black)                
		ball.update()


        frame += 1
 
	s1_superpad()
	s1_serve()
	s2_superpad()
	s2_serve()
	
        if upgrade1.time > upgradeTime:
                paddle1.size = initialSize
                upgrade1.isActive = False
                upgrade1.time = 0

        if upgrade2.time > upgradeTime:
                paddle2.size = initialSize
                upgrade2.isActive = False
                upgrade1.time = 0



      
	if paddle1.atEdge(): 
		paddle1.vert *= -1
	if paddle2.atEdge(): 
		paddle2.vert *= -1

ball.draw(black)
paddle1.draw(black)
paddle2.draw(black)
score1.draw(black)
score2.draw(black)
for i in range(1,25):
        if i % 3 != 0:
                select(40,i)
                print(black)

select(22,12)
output("\033[41m" + u+u+u+u+r+r+d+d+l+l+l + "\033[0m")
select(26,8)
output("\033[41m" + d+d+d+d+r+r+r + "\033[0m")
select(30,12)
output("\033[41m" + u+u+r+l+u+u+r+r+d+d+d+d+d + "\033[0m")
select(34,8)
output("\033[41m" + d+r+r+u+d+l+d+d+d+d + "\033[0m")
select(40,8)
output("\033[41m" + l+l+d+d+r+l+d+d+r+r+r + "\033[0m")
select(42,12)
output("\033[41m" + u+u+u+u+r+r+d+d+l+d+d + "\033[0m")
select(44,12)
output("\033[41m" + u + red[10:])
if score1.val == 9:
        select(49,8)
        output("\033[41m" + r+d+d+d+d+d + "\033[0m")        
else:
        select(50,8)
        output("\033[41m" + r+r+d+d+l+l+d+d+r+r+r + "\033[0m")
select(29,14)
output("\033[41m"+ d+d+d+r+l+d+d + "\033[0m")
select(31,16)
output("\033[41m"+ r + "\033[0m")
select(33,14)
output("\033[41m"+ d+d+d+l+r+d+d + "\033[0m")
select(35,14)
output("\033[41m"+ d+d+d+d+d + "\033[0m")
select(37,18)
output("\033[41m"+ u+u+u+r+l+u+u + "\033[0m")
select(39,16)
output("\033[41m"+ u + "\033[0m")
select(41,14)
output("\033[41m"+ d+d+d+l+r+d+d + "\033[0m")
select(45,14)
output("\033[41m" + l+l+d+d+r+r+d+d+l+l+l + "\033[0m")
select(1,81)
serialPort.close()
