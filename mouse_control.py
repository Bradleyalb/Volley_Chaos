import sys, pygame
pygame.init()
import numpy as np
size = width, height = 1300, 700
image_size = [50,50]
start__speed_x = 0
start_speed_y = 5
top_speed = 2
black = 0, 0, 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)

class Ball:
    def __init__(self,loc,speed,size):
        self.loc = loc
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load("intro_ball.gif"),image_size)
        self.angle = None
        self.collided = False

def speed_angle(speed):
    pass
def center(ball):
    return [ball.loc.right-image_size[0]/2, ball.loc.bottom-image_size[1]/2]

def get_angle(ball,other):
    return (center(ball)[0]-center(other)[0],center(ball)[1]-center(other)[1])

def distance(ball,other):
    #print(center(ball))
    return sum((np.array(center(ball))-np.array(center(other)))**2)**0.5
def update_speed(ball):
    ball.speed[1] += 0.5
    if ball.angle != None and not ball.collided:
        ball.collided = True
        velocity = (ball.angle[0]**2+ball.angle[1]**2)**0.5
        speed_vec = pygame.math.Vector2(ball.speed)
        ball.speed = speed_vec.reflect(ball.angle)
        ball.angle = None
    ball.loc = ball.loc.move(ball.speed)
    if ball.loc.left < 0 or ball.loc.right > width:
        ball.speed[0] = -ball.speed[0]
    if ball.loc.bottom > height:
        ball.speed[1] = -20
    screen.blit(ball.image, ball.loc)

def mouse_distance(ball,mouse):
    print(center(ball))
    return sum((np.array(center(ball))-np.array(mouse))**2)**0.5
def mouse_collide(ball,mouse):
    #print(sum((np.array(center(ball))-np.array(mouse))**2)**0.5)
    if sum((np.array(center(ball))-np.array(mouse))**2)**0.5 < 45:
        return True
    return False

def get_mouse_angle(ball,mouse):
    return (center(ball)[0]-mouse[0],center(ball)[1]-mouse[1])
ball_list = [Ball(pygame.Rect(x,x/2,image_size[0],image_size[1]),[start__speed_x,start_speed_y],image_size) for x in range(0,800,100)]


while True:
    clock.tick(60)
    screen.fill(black)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    pygame.draw.circle(screen,(255,0,0),mouse,20)

    for ball in ball_list:
        update_speed(ball)
    for ball in ball_list:
        angle = None
        for other in ball_list:
            if other != ball:
                if not ball.collided and ball.loc.colliderect(other.loc):
                    ball.angle = get_angle(ball,other)
        if not ball.collided and mouse_collide(ball,mouse):
            ball.angle = get_mouse_angle(ball,mouse)
        if mouse_distance(ball,mouse)> 70 and not any(distance(ball,other) < 60 for other in ball_list if ball != other):
            ball.collided = False
                
    

    pygame.display.flip()