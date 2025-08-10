import pygame
from pygame.locals import *
import sys
import os
import json
import random

def get_asset_path(filename):
    if getattr(sys,'frozen',False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path,'assets',filename)

pygame.init()
pygame.display.set_caption("Flappy Eagle")
screen = pygame.display.set_mode((1024,650))
font = pygame.font.SysFont("Segoe UI", 30)

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
high_score = 0
jump_sound = pygame.mixer.Sound(get_asset_path("flappy_whoosh-43099.wav"))
class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Eagle = pygame.image.load(get_asset_path("Eagle.png"))
        self.Eagle = pygame.transform.scale(self.Eagle, (100*2,66.641*2))
        self.EagleUp = pygame.transform.rotate(self.Eagle,30)
        self.EagleDown = pygame.transform.rotate(self.Eagle,-30)
        self.rect = self.Eagle.get_rect(center=(100,300))
        self.gravity= 0.5
        self.speedV = 10
        self.speedH = 20

def create_pipe():
    offset = random.randint(100, 200)
    pipeheight = pipe.get_height()
    y2 = random.randint(0,400)
    y1 = 600 - (y2 + offset)
    return y1 , y2
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running =False

        screen.fill((254, 254, 254))
        screen.blit(sky, (0, 0))
        screen.blit(backgroundD,(0,170))
        screen.blit(groundD,(0,550))
        pygame.display.update()

        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE | event.key == K_UP:
                height += 1
                jump_sound.play()
                pygame.display.update()


pygame.quit()
sys.exit()