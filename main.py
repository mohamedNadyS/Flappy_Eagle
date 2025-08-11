import pygame
from pygame.locals import *
import sys
import os
import json
import random

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
sky = pygame.image.load(get_asset_path("sky.png"))
sky = pygame.transform.scale(sky, (1024,600))
clock = pygame.time.Clock()
height = 0
score = 0
highscore_file = 'high_score.json'
high_score = loadHighScore()
jump_sound = pygame.mixer.Sound(get_asset_path("flappy_whoosh-43099.wav"))
gamestate = "menu"
class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Eagle = pygame.image.load(get_asset_path("Eagle.png"))
        self.Eagle = pygame.transform.scale(self.Eagle, (100*2,66.641*2))
        self.EagleUp = pygame.transform.rotate(self.Eagle,30)
        self.EagleDown = pygame.transform.rotate(self.Eagle,-30)
        self.rect = self.Eagle.get_rect(center=(100,300))
        self.gravity= 0.5
        self.maxFallSpeed = 10
        self.jumpHeight = -10
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        if self.velocity > self.maxFallSpeed:
            self.velocity = self.maxFallSpeed
        self.rect.y += self.velocity
        rotation = max(-40,min(40,self.velocity *3))
        self.Eagle = pygame.transform.rotate(self.Eagle,-rotation)
        oldcenter = self.rect.center
        self.rect = self.Eagle.get_rect(center=oldcenter)
        if self.rect.y <0:
            self.rect.top =0
            self.velocity=0
        
    def jump(self):
        self.velocity = self.jumpHeight
        if jump_sound:
            jump_sound.play()

    def getMask(self):
        return pygame.mask.from_surface(self.Eagle)

class CreatePipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.passed = False
        self.offset = random.randint(100, 200)
        self.pipeheight = pipe.get_height()
        self.y2 = random.randint(0,400)
        self.y1 = 600 - (self.y2 + self.offset)
        self.speedH = 20
        self.toppipe = pygame.transform.flip(pipe,False,True)
        self.downpipe = pipe.copy()
        self.rect1 = self.toppipe.get_rect()
        self.rect2 = self.downpipe.get_rect()

def writeText(screen,text,size,x,y,color):
    font1 = pygame.font.Font(get_asset_path("FlappybirdyRegular-KaBW.ttf"),size)
    textSurface = font1.render(text,True,color)
    textRect = textSurface.get_rect(center=(x,y))
    screen.blit(textSurface,textRect)

def drawMenu(screen):
    screen.fill((254, 254, 254))
    screen.blit(sky, (0, 0))
    screen.blit(backgroundD,(0,170))
    screen.blit(groundD,(0,550))
    writeText(screen,"Flappy Eagle",60,512,200,(255,255,255))
    writeText(screen,f"High Score: {high_score}",30,512,290,(255,255,255))
    writeText(screen,"Press SPACE or UP to start",20,512,370,(255,255,255))

def drawGameover(screen):
    screen.fill((254, 254, 254))
    screen.blit(sky, (0, 0))
    screen.blit(backgroundD,(0,170))
    screen.blit(groundD,(0,550))
    writeText(screen,"Game Over",60,512,200,(136,8,8))
    writeText(screen,f"High Score: {high_score}",30,512,370,(255,255,255))
    writeText(screen,"To restart press SPACE or UP",30,512,450,(255,255,255))
    writeText(screen,"Press ESC to return to the Menu",30,512,530,(255,255,255))

def reset():
    global score,eagle
    score = 0
    eagle = Eagle()
eagle = Eagle()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running =False
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key==K_UP:
                if gamestate == "menu":
                    gamestate = "playing"
                elif gamestate == "gameover":
                    gamestate = "playing"
                elif gamestate == "playing":
                    eagle.jump()

        if gamestate == "menu":
            drawMenu(screen)
        elif gamestate == "playing":
            eagle.update()
            "not complete"

        elif gamestate == "gameover":
            drawGameover(screen)
        pygame.display.flip()

pygame.quit()
sys.exit()