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

