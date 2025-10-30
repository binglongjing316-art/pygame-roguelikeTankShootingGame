import pygame


# 初始化精灵组
all_sprites = pygame.sprite.Group()  # 所有可见元素
enemies = pygame.sprite.Group()  # 敌人容器
bullets = pygame.sprite.Group()  # 子弹容器
walls = pygame.sprite.Group()  # 墙体容器
players = pygame.sprite.Group()
timers = pygame.sprite.Group()  # 计时器容器
booms = pygame.sprite.Group()
Texts = pygame.sprite.Group()  # 浮动文字容器
