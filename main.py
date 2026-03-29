import pygame
import sys
import os

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Цвета (для фона и текста)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Настройки экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Прыгун: монетки и портал")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)




class Player:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        #Гравитация
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False


