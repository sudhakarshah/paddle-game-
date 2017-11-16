import sys
import pygame

pygame.init()

Screen_Size=(640,480)
Paddle_Height=12
Paddle_Width=60
Ball_Diameter=16
Ball_Radius=Ball_Diameter//2
Max_Paddle_X=Screen_Size[0]-Paddle_Height
Max_Ball_X=Screen_Size[0]-Ball_Diameter
Max_Ball_Y=Screen_Size[1]-Ball_Diameter
Down_Paddle_Y=470
Up_Paddle_Y=10
Up_P_Dest=300
Ball_Velocity=[5,-5]

Black = (0,0,0)
White = (255,255,255)
Blue = (0,0,255)

x=435 #claculation (Distance travelled by the ball after hitting the down paddle and then going up)

Game_State=False

Up_Paddle=pygame.Rect(450,Up_Paddle_Y,Paddle_Width+30,Paddle_Height)
Down_Paddle=pygame.Rect(300,Down_Paddle_Y,Paddle_Width,Paddle_Height)
Ball=pygame.Rect(300+Paddle_Width//2,Down_Paddle_Y - Ball_Diameter,Ball_Diameter,Ball_Diameter)


Screen=pygame.display.set_mode(Screen_Size)
pygame.display.set_caption("Paddle Game")
clock=pygame.time.Clock()
Screen.fill(Black)


# Draw paddle
pygame.draw.rect(Screen, Blue ,Up_Paddle)
pygame.draw.rect(Screen, Blue, Down_Paddle)

# Draw ball
pygame.draw.circle(Screen, White, (Ball.left + Ball_Radius, Ball.top + Ball_Radius), Ball_Radius)




def initial_state():
	global Down_Paddle

	Up_Paddle_Y=10
	Ball.left=300+(Paddle_Width//2)
	#Ball.top=Down_Paddle_Y - Ball_Diameter
	Ball.top=449 #calculations
	Down_Paddle.left=300




def game_play():
	global Game_State,clock,Screen,Up_Paddle


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		clock.tick(50)
		Screen.fill(Black)			
		check_input()
		move_ball()
		collision()

		if (Ball.top>480):
			Game_State= False
			Ball_Velocity[1]=-Ball_Velocity[1]
			initial_state()
			Up_Paddle.left=decide_position(x)-(Paddle_Width//2);

		elif (Ball.top<0):
			Game_State=False
			initial_state()
			Up_Paddle.left=decide_position(x)-(Paddle_Width//2);


		# Draw paddle
		pygame.draw.rect(Screen, Blue ,Up_Paddle)
		pygame.draw.rect(Screen, Blue, Down_Paddle)
		# Draw ball
		pygame.draw.circle(Screen, White, (Ball.left + Ball_Radius, Ball.top + Ball_Radius), Ball_Radius)

		pygame.display.flip()




def check_input():
	global Game_State,Down_Paddle,Up_Paddle

	user_input=pygame.key.get_pressed()

	if (user_input[pygame.K_LEFT]):
		Down_Paddle.left-=5
		if Down_Paddle.left<0:
			Down_Paddle.left=0
	if (user_input[pygame.K_RIGHT]):
		Down_Paddle.left+=5
		if Down_Paddle.left+Paddle_Width>Max_Paddle_X:
			Down_Paddle.left=Max_Paddle_X-Paddle_Width

	if (user_input[pygame.K_SPACE]):
		Game_State= not Game_State




def move_ball():
	global Ball,Game_State

	if (Game_State==True):

		Ball.left+=Ball_Velocity[0]
		Ball.top+=Ball_Velocity[1]

		if Ball.left<0:
			Ball.left=0
			Ball_Velocity[0]=-Ball_Velocity[0]
		elif Ball.left>Max_Ball_X:
			Ball.left=Max_Ball_X
			Ball_Velocity[0]=-Ball_Velocity[0]

		#if Ball.top>Max_Ball_Y:
		#	Ball.top=Max_Ball_Y
			#Ball_Velocity[1]=-Ball_Velocity[1]


def collision():
	global Ball,Ball_Velocity,Up_P_Dest,Up_Paddle



	if (Ball.colliderect(Up_Paddle)):
		#Ball.top=Up_Paddle_Y
		Ball_Velocity[1]=-Ball_Velocity[1]

	elif (Ball.colliderect(Down_Paddle)):
		Ball_Velocity[1]=-Ball_Velocity[1]

		#
		#print (decide_position(x)-(Paddle_Width//2))
		if (decide_position(x)-(Paddle_Width//2)<0):
			Up_Paddle.left=0
		elif (decide_position(x)-(Paddle_Width//2)>580):
			Up_Paddle.left=580
		else:
			Up_Paddle.left=decide_position(x)-(Paddle_Width//2); # deciding the postion of the above paddle upon collision of ball with lower paddle
		print (Up_Paddle.left)

		
def decide_position(x):
	if (Ball_Velocity[0]>0):

		if (Screen_Size[0]-Ball.left>x):
			Up_P_Dest= Ball.left+x
		else:
			Up_P_Dest=Screen_Size[0]-(x-(Screen_Size[0]-Ball.left))
	
	else:
		if (Ball.left>x):
			Up_P_Dest= Ball.left-x
		else:
			Up_P_Dest=x-Ball.left
	if (Up_P_Dest+Paddle_Width>Screen_Size[0]):
		Up_P_Dest=Screen_Size[0]-Paddle_Width
	elif(Up_P_Dest<0):
		Up_P_Dest=0
	return (Up_P_Dest)


game_play()


