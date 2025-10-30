import pygame
import colorsys
import math
from include import constant, variable
from include.sprites_init import players, enemies


class Bullet(pygame.sprite.Sprite):
    """子弹类"""

    def __init__(self, x, y, direction, damage, label=None, move_direction_dx_dy=(0, 0), tank_speed=0.0,
                 deviation_angle=0.0, speed=5.0, bullet_range=9999):
        """
        初始化子弹
        :param x: 生成x坐标
        :param y: 生成y坐标
        :param direction: 子弹方向
        :param damage: 子弹伤害
        :param label: 子弹标记
        :param move_direction_dx_dy: 坦克移动方向
        :param tank_speed: 坦克移动速度
        :param deviation_angle: 子弹偏移角度
        :param speed: 子弹速度
        """
        super().__init__()
        if label is None:
            label = []
        self.label = label  # 子弹标记
        self.size = (1 - 1000 / (damage + 1000)) * 80 + 8  # 伤害无穷时，子弹尺寸为80+8，伤害为0时，子弹尺寸为8
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)  # 透明
        # 设置颜色
        self.hue = 0
        bullet_color = constant.RED if 'enemy' in label else constant.WHITE
        # 绘制圆形
        pygame.draw.circle(self.image, bullet_color, (self.size / 2, self.size / 2), self.size / 2)
        self.rect = self.image.get_rect(center=(x, y))  # 初始位置
        self.speed = speed  # 飞行速度
        self.dx = 0
        self.dy = 0
        if self.speed <= 1:
            self.speed = 1
        self.tank_speed = float(tank_speed)  # 坦克移动速度
        self.existence_time = 5 * bullet_range / self.speed  # 存在时间(帧数)
        self.direction = direction  # 飞行方向

        self.damage = damage  # 伤害设置

        # 穿透子弹
        self.penetrate = False
        # 追踪子弹
        self.track = False
        self.track_power = 1
        player = None
        for player in players:
            pass
        if "penetrate" in player.card_functions_list or "borer" in player.card_functions_list:
            self.penetrate = True if 'player' in label else False
        if "consciousness" in player.card_functions_list:
            if 'player' in label:
                self.track = True
                self.track_power = player.card_functions_list.count("consciousness")

        self.hit_targets = set()  # 记录已命中目标的唯一标识
        self.move_direction_dx = move_direction_dx_dy[0]
        self.move_direction_dy = move_direction_dx_dy[1]

        # 偏移角度
        self.deviation_angle = deviation_angle

    def update(self):
        """子弹更新"""
        if self.track:
            # 变色子弹
            # 更新色相值（调整步长可以改变颜色变化速度）
            self.hue = (self.hue + 3) % 360
            # 将HSV转换为RGB（hsv_to_rgb需要0-1范围的参数）
            r, g, b = colorsys.hsv_to_rgb(self.hue / 360, 1, 1)
            # 转换为0-255范围的整数
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            # 绘制圆形
            pygame.draw.circle(self.image, (r, g, b), (self.size // 2, self.size // 2), self.size // 2)
        elif "boss1" in self.label:
            # 更新色相值（调整步长可以改变颜色变化速度）
            self.hue = (self.hue + 3) % 360
            # 将HSV转换为RGB（hsv_to_rgb需要0-1范围的参数）
            r, g, b = colorsys.hsv_to_rgb(self.hue / 360, 1, 1)
            # 转换为0-255范围的整数
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            # 绘制圆形
            pygame.draw.circle(self.image, (g, r, b), (self.size // 2, self.size // 2), self.size // 2)
        else:
            pass
        # 根据方向设置初始速度
        if self.dx == 0 and self.dy == 0:
            if self.direction == "up":
                angle_rad = math.radians(self.deviation_angle + 90)
                self.dx = math.cos(angle_rad) * self.speed
                self.dy = math.sin(angle_rad) * self.speed
            elif self.direction == "down":
                angle_rad = math.radians(self.deviation_angle + 270)
                self.dx = math.cos(angle_rad) * self.speed
                self.dy = math.sin(angle_rad) * self.speed
            elif self.direction == "left":
                angle_rad = math.radians(self.deviation_angle + 180)
                self.dx = math.cos(angle_rad) * self.speed
                self.dy = math.sin(angle_rad) * self.speed
            elif self.direction == "right":
                angle_rad = math.radians(self.deviation_angle)
                self.dx = math.cos(angle_rad) * self.speed
                self.dy = math.sin(angle_rad) * self.speed
            else:
                self.dx = 0
                self.dy = 0
            # 根据坦克移动方向偏移
            if 'player' in self.label:
                dv_x = self.move_direction_dx * self.tank_speed * 0.5
                dv_y = self.move_direction_dy * self.tank_speed * 0.5
            else:
                dv_x = 0
                dv_y = 0
            self.dx += dv_x
            self.dy -= dv_y

        # 追踪
        if self.track:
            if 'player' in self.label:
                # 检测最近敌人
                min_distance = 999999999999
                min_rect = None
                for enemy in enemies:
                    Dx = enemy.rect.centerx - self.rect.centerx
                    Dy = enemy.rect.centery - self.rect.centery
                    if min_distance > (Dx ** 2 + Dy ** 2) ** 0.5:
                        min_distance = (Dx ** 2 + Dy ** 2) ** 0.5
                        min_rect = (enemy.rect.centerx, enemy.rect.centery)
                # 追踪
                if min_rect is None:
                    pass
                else:
                    self.track_power = 5 if self.track_power > 5 else self.track_power
                    if variable.index % (5 // self.track_power) == 0:
                        if self.rect.centerx > min_rect[0]:
                            self.dx -= 1
                        else:
                            self.dx += 1
                        if self.rect.centery > min_rect[1]:
                            self.dy += 1
                        else:
                            self.dy -= 1
            elif 'enemy' in self.label:
                # 检测最近玩家
                min_distance = 999999999999
                min_rect = None
                for player in players:
                    Dx = player.rect.centerx - self.rect.centerx
                    Dy = player.rect.centery - self.rect.centery
                    if min_distance > (Dx ** 2 + Dy ** 2) ** 0.5:
                        min_distance = (Dx ** 2 + Dy ** 2) ** 0.5
                        min_rect = (player.rect.centerx, player.rect.centery)
                # 追踪
                if min_rect is None:
                    pass
                else:
                    self.track_power = 5 if self.track_power > 5 else self.track_power
                    if variable.index % 5 // self.track_power == 0:
                        if self.rect.centerx > min_rect[0]:
                            self.dx -= 1
                        else:
                            self.dx += 1
                        if self.rect.centery > min_rect[1]:
                            self.dy += 1
                        else:
                            self.dy -= 1
        # 移动
        self.rect.x += self.dx
        self.rect.y -= self.dy
        # 移出屏幕后自动销毁
        if not constant.virtual_screen.get_rect().colliderect(self.rect):
            if not self.track:
                self.kill()
        # 存在时间结束后自动销毁
        if self.existence_time <= 0:
            self.kill()
        self.existence_time -= 1
