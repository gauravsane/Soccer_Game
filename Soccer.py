import pygame
from pygame import *

pygame.init()


clock = pygame.time.Clock()


screen_x = 827    #width
screen_y = 500    #height

screen = pygame.display.set_mode((screen_x, screen_y))  #game screen
pygame.display.set_caption('Soccer Game')
pygame.display.set_icon(pygame.image.load('D:/Python/Hw/Project2/icon.jpg'))

#define font
font = pygame.font.SysFont('Bauhaus 93', 30)
font1 = pygame.font.SysFont('Goudy Stout', 20)



#define colors
red = (204, 0, 0)
green = (247, 255, 0)


#variables
live_ball = False
cpu_score = 0
player_score = 0
title = 'CPU: '
title1 = 'PLAYER: '
fps = 80
score = 0
margin = 20
ball_x = 580
ball_y = 250
winner = 0
speed_increase = 0


#images
bg_img = pygame.image.load('D:/Python/Hw/Project2/soccer.jpg')
goal_post_right = pygame.image.load('D:/Python/Hw/Project2/goalRight1.png').convert()
goal_post_left = pygame.image.load('D:/Python/Hw/Project2/goalLeft1.png').convert()
player_img = pygame.image.load('D:/Python/Hw/Project2/shinchan1.png')
cpu_img = pygame.image.load('D:/Python/Hw/Project2/kazama2.png')
soccer_img = pygame.image.load('D:/Python/Hw/Project2/ball.png')

#collide to goal_post
##collide = pygame.rect.colliderect(goal_post_right.rect)
##collide1 = pygame.rect.colliderect(goal_post_left)


def draw_ground():
    screen.blit(bg_img, (0, 0))
    screen.blit(goal_post_right, (700,136))
    screen.blit(goal_post_left, (-25,136))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Characters():
    def __init__(self, x, y, image):
        self.reset(x, y, image)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < 475:
            self.rect.move_ip(0, self.speed)

    def ai(self):
        #ai move automatically
        #move up
        if self.rect.centery > soccer_ball.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)
        #move down
        if self.rect.centery < soccer_ball.rect.top and self.rect.top < 330:
            self.rect.move_ip(0, self.speed) 

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def reset(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

##    def reset(self):
        

class ball():
    def __init__(self, x, y, image):
        self.reset(x, y, image)

    def move(self):                     #for collision detection
        #collision with top margin
        if self.rect.top < margin:
            self.speed_y *= -1
            
        #collision with bottom of screen
        if self.rect.bottom > screen_y:
            self.speed_y *= -1

        if self.rect.colliderect(player_char) or self.rect.colliderect(cpu_char):
            self.speed_x *= -1

        
        #collision   
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > screen_x:
            self.winner = -1
       
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def reset(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = -2.5
        self.speed_y = 2.5
        self.winner = 0 #1 means player scored is 1 and cpu is -1
        
#create characters
player_char = Characters(640, 180, player_img)
cpu_char = Characters(120, 170, cpu_img)

soccer_ball = ball(ball_x, ball_y, soccer_img)

run = True

while run:
    clock.tick(fps)
    
    draw_ground()

    #cpu score
    draw_text('CPU: '+ str(cpu_score), font, green, 190 , 470)

    #player score
    draw_text('Player: '+ str(player_score), font, green, 560, 470)

    #ball speed counter
    draw_text('Ball Speed: '+ str(abs(soccer_ball.speed_x)), font, green, 320, 0.4)

    #draw player
    player_char.draw()
    
    #draw cpu
    cpu_char.draw()


    if live_ball == True:
        speed_increase += 1
        winner = soccer_ball.move()
        if winner == 0:
            #draw a ball
            soccer_ball.draw()
            #for moving a player up and down
            player_char.move()
            cpu_char.ai()

        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                cpu_score += 1
                

    if live_ball == False:
        path = 'D:/Python/Hw/Project2/Theme.mp3'
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        if winner == 0:
            draw_text('CLICK ANYWHERE TO START', font1, red, 150, 140)
        if winner == 1:
            draw_text('YOU SCORED', font1, red, 150, 140)
            draw_text('CLICK ANYWHERE TO START', font, red, 150, 170)
            
        if winner == -1:
            draw_text('CPU SCORED', font1, red, 330, 140)
            draw_text('CLICK ANYWHERE TO START', font1, red, 150, 170)
        
##    soccer_ball.move()

    

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            soccer_ball.reset(530, 250, soccer_img)
            player_char.reset(640, 180, player_img)
            cpu_char.reset(120, 170, cpu_img)
            
            
            
            
    if speed_increase > 500:
        speed_increase = 0
        if soccer_ball.speed_x < 0:
            soccer_ball.speed_x -= 1
        if soccer_ball.speed_x > 0:
            soccer_ball.speed_x += 1
        if soccer_ball.speed_y < 0:
            soccer_ball.speed_y -= 1
        if soccer_ball.speed_y < 0:
            soccer_ball.speed_y += 1

    
    pygame.display.update()

    
pygame.quit()
