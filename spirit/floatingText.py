import pygame
from include import constant


class FloatingText(pygame.sprite.Sprite):
    """浮动文本类"""

    def __init__(self, x, y, txt, color=constant.RED):
        super().__init__()
        self.font = pygame.font.Font(None, 28)  # 伤害数字字体
        if type(txt) == int or type(txt) == float:
            self.image = self.font.render(f"{round(txt)}", True, color)  # 渲染文本表面
        else:
            self.image = self.font.render(f"{txt}", True, color)  # 渲染文本表面
        self.rect = self.image.get_rect(center=(x, y))
        self.float_speed = 1.5  # 上浮速度
        self.lifetime = 120  # 存在时间（帧数）
        self.alpha = 255  # 初始不透明度

    def update(self):
        # 上浮效果
        self.rect.y -= self.float_speed
        # 渐隐效果
        self.alpha = max(0, self.alpha - 255 // self.lifetime)
        self.image.set_alpha(self.alpha)
        # 生命周期结束自动移除
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()