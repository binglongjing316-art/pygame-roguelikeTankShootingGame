import pygame
from include import constant
from include.sprites_init import enemies, walls, Texts, players
from include import variable

from spirit.floatingText import FloatingText
from spirit.tank import Tank

body_image = pygame.image.load("image/boom/boom.png")
frame_count = 4
frame_type_count = 2
# 每帧宽，高
frame_width, frame_height = body_image.get_width() // frame_count, body_image.get_height() // frame_type_count
# 不同状态的帧图像
frames_r = []
frames_l = []
frames_u = []
frames_d = []
# 提取第一行的4帧
for col in range(frame_count):
    frame = body_image.subsurface(
        col * frame_width,  # x坐标
        0,  # y坐标（第一行）
        frame_width,
        frame_height
    )
    frames_r.append(frame)
    frame = body_image.subsurface(
        (frame_count - col - 1) * frame_width,  # x坐标
        0,  # y坐标（第一行）
        frame_width,
        frame_height
    )
    frames_l.append(frame)
    frame = body_image.subsurface(
        col * frame_width,  # x坐标
        frame_height,  # y坐标（第二行）
        frame_width,
        frame_height
    )
    frames_d.append(frame)
    frame = body_image.subsurface(
        (frame_count - col - 1) * frame_width,  # x坐标
        frame_height,  # y坐标（第二行）
        frame_width,
        frame_height
    )
    frames_u.append(frame)
boom_image = frames_r[3]


class Boom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 600  # 真实尺寸
        self.circle_size = 20  # 圆尺寸
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)  # 透明
        # 设置颜色
        self.red = 0  # 红值
        color = (255, 255 - self.red, 255 - self.red)
        pygame.draw.circle(self.image, color, (self.size / 2, self.size / 2), self.size / 2)
        self.rect = self.image.get_rect(center=(x, y))  # 初始位置
        #
        self.direct = None
        self.speed = 0
        self.explosion_time = 0  # 爆炸时间计数
        self.explosion_delay = 180  # 爆炸延迟时间（帧数）
        self.explosion_range = self.circle_size // 2  # 爆炸半径
        self.damage = 20  # 爆炸起始伤害

    def explode(self):
        # 一次性伤害与破坏
        impacts = pygame.sprite.Group()
        impacts.add(enemies)
        impacts.add(players)
        impacts.add(walls)
        for impact_object in impacts:
            distance = ((impact_object.rect.centerx - self.rect.centerx) ** 2 + (
                    impact_object.rect.centery - self.rect.centery) ** 2) ** 0.5
            self.explosion_range = self.circle_size // 2  # 爆炸半径
            if distance < self.explosion_range:
                impact_object.health -= self.damage
                if isinstance(impact_object, Tank):
                    # 伤害数字生成
                    damage_text = FloatingText(
                        impact_object.rect.right + 10,  # 右侧偏移
                        impact_object.rect.top - 10,  # 顶部上方
                        self.damage,
                        constant.RED
                    )
                    Texts.add(damage_text)
        self.kill()

    def update(self):
        if self.explosion_time < self.explosion_delay:
            self.explosion_time += 1
        else:
            self.explode()

        # 爆炸过程变化
        self.red += 2
        player = None
        for player in players:
            pass
        self.damage += player.level / 20
        # 移动
        i = variable.index // 5 % frame_count
        if self.direct == "right":
            self.rect.x += self.speed
            _frame = frames_r[i]
        elif self.direct == "left":
            self.rect.x -= self.speed
            _frame = frames_l[i]
        elif self.direct == "up":
            self.rect.y -= self.speed
            _frame = frames_u[i]
        elif self.direct == "down":
            self.rect.y += self.speed
            _frame = frames_d[i]
        else:
            _frame = boom_image

        if self.red > 255:
            self.red = 255
        self.circle_size += 3

        color = (255, 255 - self.red, 255 - self.red)
        #
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)  # 透明
        pygame.draw.circle(self.image, color, (self.size // 2, self.size // 2), self.circle_size / 2)
        self.image.blit(_frame, (self.size // 2 - frame_width // 2, self.size // 2 - frame_width // 2))
