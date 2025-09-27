import pygame
from pygame.locals import *
import sys
import os
import json
import random
import time

def loadHighScore():
    try:
        with open('high_score.json','r') as f:
            return json.load(f)['high_score']
    except (FileNotFoundError,json.JSONDecodeError):
        return 0
def saveHighscore(score):
    with open('high_score.json','w') as f:
        json.dump({'high_score':score},f)


def get_asset_path(filename):
    if getattr(sys,'frozen',False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path,'assets',filename)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Flappy Eagle")
screen = pygame.display.set_mode((1024,650))

backgroundL = pygame.image.load(get_asset_path("background_light.jpeg"))
backgroundD = pygame.image.load(get_asset_path("background_dark.png"))
groundD = pygame.image.load(get_asset_path("ground_dark3.png"))
groundD = pygame.transform.scale(groundD, (1024, 100))
groundL = pygame.image.load(get_asset_path("ground_light1.png"))
pipe = pygame.image.load(get_asset_path("pipe.png"))
pipe = pygame.transform.scale(pipe,(150,500))
pipes = []
pipeFrequency = 90
pipeTimer = 0
sky = pygame.image.load(get_asset_path("sky.png"))
sky = pygame.transform.scale(sky, (1024,600))
clock = pygame.time.Clock()
height = 0
score = 0
highscore_file = 'high_score.json'
high_score = loadHighScore()
jump_sound = pygame.mixer.Sound(get_asset_path("flappy_whoosh-43099.wav"))
die_sound = pygame.mixer.Sound(get_asset_path("tonic-bonk.mp3"))
gamestate = "menu"

class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Eagle = pygame.image.load(get_asset_path("Eagle.png"))
        self.Eagle = pygame.transform.scale(self.Eagle, (100*2,66.641*2))
        self.Eagle_copy = self.Eagle.copy()
        self.EagleUp = pygame.transform.rotate(self.Eagle,30)
        self.EagleDown = pygame.transform.rotate(self.Eagle,-30)
        self.rect = self.Eagle_copy.get_rect(center=(200,325))
        self.current_rotation =0
        self.gravity= 0.8
        self.maxFallSpeed = 10
        self.jumpHeight = -12
        self.velocity = 0
        self.collesion_rect = pygame.Rect(0,0,int(self.rect.width*0.7),int(self.rect.height*0.7))

        self.rotated_images={}
        for angle in range(-40,41,5):
            self.rotated_images[angle]= pygame.transform.rotate(self.Eagle,-angle)

    def update(self):
        self.velocity += self.gravity
        if self.velocity > self.maxFallSpeed:
            self.velocity = self.maxFallSpeed
        self.rect.y += self.velocity
        rotation = max(-40,min(40,self.velocity *3))
        roundedvalue = round(rotation/5)*5
        self.collesion_rect.center = self.rect.center
        if abs(roundedvalue -self.current_rotation) >= 5:
            self.current_rotation = roundedvalue
            self.Eagle_copy= self.rotated_images[self.current_rotation]
            oldcenter = self.rect.center
            self.rect = self.Eagle_copy.get_rect(center=oldcenter)
        if self.rect.y <0:
            self.rect.top =0
            self.velocity=0
        
    def jump(self):
        self.velocity = self.jumpHeight
        if jump_sound:
            jump_sound.play()

    def getMask(self):
        return pygame.mask.from_surface(self.Eagle_copy)

class CreatePipe(pygame.sprite.Sprite):
    def __init__(self,xposition):
        super().__init__()
        self.passed = False
        self.offset =220
        self.gapYposition = random.randint(130, 340)
        self.x = xposition
        self.speedH = 4

        self.toppipe = pygame.transform.flip(pipe,False,True)
        self.downpipe = pipe.copy()

        self.rectTop = self.toppipe.get_rect()
        self.rectTop.x = self.x
        self.rectTop.bottom = self.gapYposition
        self.rectDown = self.downpipe.get_rect()
        self.rectDown.x = self.x
        self.rectDown.top = self.gapYposition + self.offset
        self.rect = pygame.Rect(self.x,0,150,650)
        self.topmask = pygame.mask.from_surface(self.toppipe)
        self.downmask = pygame.mask.from_surface(self.downpipe)

        self.collesion_rect_top = pygame.Rect(self.rectTop.x + 20, self.rectTop.y + 20, self.rectTop.width - 40, self.rectTop.height - 20)
        self.collesion_rect_down = pygame.Rect(self.rectDown.x + 20, self.rectDown.y + 20, self.rectDown.width - 40, self.rectDown.height - 20)

    def update(self):
        self.x -= self.speedH
        self.rectTop.x = self.x
        self.rectDown.x = self.x
        self.rect.x = self.x
    
    def draw(self,screen):
        screen.blit(self.toppipe,self.rectTop)
        screen.blit(self.downpipe,self.rectDown)

    def collideswith(self,eagle):
        if eagle.collesion_rect.colliderect(self.collesion_rect_top):
            return True
        if eagle.collesion_rect.colliderect(self.collesion_rect_down):
            return True
        return False


def writeText(screen,text,size,x,y,color,font="font1"):
    fon2 = pygame.font.get_default_font()
    font1 = pygame.font.Font(get_asset_path("FlappybirdyRegular-KaBW.ttf"),size)
    if font == "font2":
        font1 = pygame.font.Font(fon2,size)
    textSurface = font1.render(text,True,color)
    textRect = textSurface.get_rect(center=(x,y))
    screen.blit(textSurface,textRect)

def drawMenu(screen):
    screen.fill((254, 254, 254))
    screen.blit(sky, (0, 0))
    screen.blit(backgroundD,(0,170))
    screen.blit(groundD,(0,550))
    writeText(screen,"Flappy Eagle",100,512,200,(0,0,0))
    writeText(screen,f"High Score: {high_score}",60,512,290,(0,0,0),"font2")
    writeText(screen,"Press SPACE or UP to start",60,512,370,(0,0,0))

def drawGameover(screen):
    screen.fill((254, 254, 254))
    screen.blit(sky, (0, 0))
    screen.blit(backgroundD,(0,170))
    screen.blit(groundD,(0,550))
    writeText(screen,"Game Over",60,512,200,(136,8,8))
    writeText(screen,f"Score: {score}",40,512,290,(255,255,255),"font2")
    writeText(screen,f"High Score: {high_score}",30,512,370,(255,255,255),"font2")
    writeText(screen,"To restart press SPACE or UP",30,512,450,(255,255,255))
    writeText(screen,"Press ESC to return to the Menu",30,512,530,(255,255,255))

def drawplaying(screen):
    screen.fill((255,255,255))
    screen.blit(sky,(0,0))
    screen.blit(backgroundD,(0,170))
    screen.blit(groundD,(0,550))
    for pipeobj in pipes:
        pipeobj.draw(screen)
    screen.blit(eagle.Eagle_copy,eagle.rect)
    writeText(screen,f"Score: {score}",40,100,50,(255,255,255))

def reset():
    global score,eagle, pipes, pipeTimer
    score = 0
    eagle = Eagle()
    pipes = []
    pipeTimer = 0

eagle = Eagle()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running =False
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key==K_UP:
                if gamestate == "menu":
                    gamestate = "playing"
                    reset()
                elif gamestate == "gameover":
                    gamestate = "playing"
                    reset()
                elif gamestate == "playing":
                    eagle.jump()
            if event.key == K_ESCAPE:
                if gamestate == "gameover":
                    gamestate ="menu"


    if gamestate == "menu":
        drawMenu(screen)
    elif gamestate == "playing":
        eagle.update()
        pipeTimer+=1
        if pipeTimer >=pipeFrequency:
            pipes.append(CreatePipe(1024))
            pipeTimer =0
        for pipeO in pipes[:]:
            pipeO.update()
            if pipeO.x < -150:
                pipes.remove(pipeO)
                continue
            if not pipeO.passed and pipeO.x +75<eagle.rect.centerx:
                pipeO.passed = True
                score +=1
        
        collision = False
        for pipeO in pipes:
            if pipeO.x < eagle.rect.x + 70 and pipeO.x > eagle.rect.x - 120:
                if pipeO.collideswith(eagle):
                    collision = True
                    break
        if eagle.rect.bottom >= 645:
            collision = True
        if collision:
            if die_sound:
                die_sound.play()
                time.sleep(0.25)
            gamestate ="gameover"
            if score > high_score:
                high_score = score
                saveHighscore(high_score)
        drawplaying(screen)
            

    elif gamestate == "gameover":
        drawGameover(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()