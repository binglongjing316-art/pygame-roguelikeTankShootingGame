import random
import pygame

from include import constant

from include.sprites_init import timers
from spirit.timer import Timer


class Wall(pygame.sprite.Sprite):
    """墙体类，用于创建不可穿透的障碍物"""

    def __init__(self, x, y):
        """
        初始化墙体
        :param x: 墙体左上角x坐标
        :param y: 墙体左上角y坐标
        """
        super().__init__()

        self.size = 40  # 墙体尺寸
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.color = (55, 50, random.randint(100, 255))
        self.lucency = 0
        self.image.fill(self.color)  # 填充颜色
        self.rect = self.image.get_rect(topleft=(x, y))  # 设置初始位置
        self.health = 80
        self.health_max = 80
        grid_x = x // constant.GRID_SIZE
        grid_y = y // constant.GRID_SIZE
        constant.grid[grid_x][grid_y] = 1  # 标记为障碍

    def update(self):
        if self.health <= 0:
            # 清除障碍标记
            grid_x = self.rect.x // constant.GRID_SIZE
            grid_y = self.rect.y // constant.GRID_SIZE
            constant.grid[grid_x][grid_y] = 0  # 清除障碍标记

        # 墙体血量显示
        health_color_lucency = int(self.health / self.health_max * 255)  # 颜色与生命值相关
        if self.health <= 0:
            health_color_lucency = 0
        if self.lucency > health_color_lucency:
            self.lucency -= 10
        elif self.lucency < health_color_lucency:
            self.lucency += 1
        if self.lucency <= 0:
            self.lucency = 0
            self.kill()
            # 启动重生计时器
            respawn_timer = Timer(20, f"wall_respawn_{self.rect.x}_{self.rect.y}")
            timers.add(respawn_timer)
        self.image.fill((self.color[0], self.color[1], self.color[2], self.lucency))
