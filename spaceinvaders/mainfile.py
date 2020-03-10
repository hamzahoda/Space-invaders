import pygame
import math
import random
from pygame import mixer
# intialize the pygame
pygame.init()

# create the screen method hai display.set_mode aur bracket ke andar bracket aur isme height aur width
screen=pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load("background.png")


#Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)


#Caption and Icon

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load("space-invaders.png")
playerX=370
playerY=480
playerX_change=0

#Enemy        randint for random integer
enemyImg = []
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
#instead of = use .append for adding to list you dont need .append with x and y change values as they are constant but just for simplicity we are doing 
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy (1).png"))
    enemyX.append(random.randint(0,370))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(6)
    enemyY_change.append(40)   #pixels move down

#Bullet
#Ready -> you can't see the bullent on the screen
#Fire -> the bullet is currently moving 
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10 
bullet_state="Ready"


#Score
score_value = 0
#only font pygame provides you can download more and 32 is size
font = pygame.font.Font("freesansbold.ttf",32)

#Game Over text
over_font = pygame.font.Font("freesansbold.ttf",64)


#coordinates 
textx=10
testy=10

def show_score(x,y):
    score=font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text, (200,250))


def Player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))    

def fire_bullet(x,y):
    global bullet_state 
    bullet_state= "Fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,playerX,playerY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False        


#gameLoop
running=True

while running:
    #RGB- RED,GREEN,BLUE
    screen.fill((0,0,0))

    #Background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
    #if key stroke is pressed check wheter its right or left
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 7
                print("Left key is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change += 7
                print("Right key is pressed") 
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    bullet_sound=mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current x coordinate of the space ship
                    bulletX= playerX
                    fire_bullet(bulletX,bulletY)    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("key is released")




    # checking for boundaries of spaceship so it does not go out of bounds
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX=736    

    #Enemy Movement        which enemy
    for i in range(num_of_enemies):


        #Game Over       kia likhen ke game over enemy ke spacechip par poohnchne ke baad hou poochna hai
        
        if enemyY[i] > 440 :
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break    

        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 6
            enemyY[i] +=enemyY_change[i] 
        elif enemyX[i] >=736:
            enemyX_change[i] = -6 
            enemyY[i] +=enemyY_change[i] 

        #Collision
        Collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if Collision:
            explosion=mixer.Sound("explosion.wav")
            explosion.play()
            bulletY=480
            bullet_state="Ready"
            score_value +=1
            enemyX[i]=random.randint(0,370)
            enemyY[i]=random.randint(50,150)        

        enemy(enemyX[i],enemyY[i],i)    

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state="Ready"


    if bullet_state is "Fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change   

    




    Player(playerX,playerY)
    show_score(textx,testy)
    pygame.display.update()        
