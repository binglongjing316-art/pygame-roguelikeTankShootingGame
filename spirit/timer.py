import pygame
from include import variable, constant


class Timer(pygame.sprite.Sprite):
    """计时器类"""

    def __init__(self, seconds, label):
        """
        初始化计时器
        :param seconds: 计时时长(秒)
        :param label: 计时器标识(用于事件判断)
        """
        super().__init__()
        self.start_frame = variable.index
        self.frame_number = seconds * constant.FPS  # 计时器帧数
        self.is_expire = False  # 计时器到期
        self.label = label  # 计时器标签

    def update(self):
        if variable.index - self.start_frame >= self.frame_number:
            self.is_expire = True
