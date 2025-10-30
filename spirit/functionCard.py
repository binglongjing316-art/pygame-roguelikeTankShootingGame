import pygame

from include import constant


def _split_text(font, text, max_width, words_spilt=" "):
    """将文本分割为多行，处理长单词避免死循环"""
    lines = []
    words = text.split()

    while words:
        line = []
        while words:
            current_word = words[0]
            # 测试当前行加上当前单词后的宽度
            test_line = words_spilt.join(line + [current_word])
            test_width = font.size(test_line)[0]

            if test_width <= max_width:
                line.append(words.pop(0))
            else:
                # 如果当前行无法容纳当前单词
                if not line:
                    # 当前行是空的，分割长单词
                    # 找到可以放入的最大前缀
                    split_index = 1
                    while split_index <= len(current_word):
                        substring = current_word[:split_index]
                        if font.size(substring)[0] > max_width:
                            split_index -= 1
                            break
                        split_index += 1
                    # 处理无法分割的情况（如字符过宽）
                    split_index = max(split_index, 1)  # 至少分割一个字符
                    line.append(current_word[:split_index])
                    # 将剩余部分作为新单词放回列表
                    remaining = current_word[split_index:]
                    words[0] = remaining
                    # 添加当前行并清空
                    lines.append(words_spilt.join(line))
                    line = []
                break
        # 添加非空行
        if line:
            lines.append(words_spilt.join(line))
    return lines


class FunctionCard(pygame.sprite.Sprite):
    """功能卡类"""

    def __init__(self, index, data):
        super().__init__()
        self.size = (200, 300)
        self.image = pygame.Surface(self.size)
        if data["level"] == 4:
            self.color = (255, 0, 0)
        elif data["level"] == 3:
            self.color = (255, 127, 0)
        elif data["level"] == 2:
            self.color = (255, 0, 255)
        elif data["level"] == 1:
            self.color = (0, 0, 255)
        else:
            self.color = (0, 155, 0)

        self.image.fill(self.color)
        self.rect = self.image.get_rect(
            center=(constant.SCREEN_WIDTH // 2 + (index - 1) * 250, constant.SCREEN_HEIGHT // 2))
        # 绘制文字
        self._render_text(data["name"])
        self.index = index
        self.function = data
        font = pygame.font.Font(None, 36)
        text = font.render(str(index + 1), True, constant.WHITE)
        text_rect = text.get_rect(centerx=self.rect.width // 2, centery=self.rect.height - text.get_height())
        self.image.blit(text, text_rect)

    def _render_text(self, text):
        """渲染带自动换行的文本"""
        font = pygame.font.Font(None, 36)
        max_width = self.size[0] - 20  # 左右保留10像素边距

        # 分割文本为多行
        lines = _split_text(font, text, max_width)

        # 计算文本总高度
        line_height = font.get_height()
        text_height = len(lines) * line_height

        # 计算起始Y坐标（垂直居中）
        start_y = self.rect.height // 2 - text_height // 2

        # 绘制每一行
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, constant.WHITE)
            text_rect = text_surface.get_rect(
                centerx=self.rect.width // 2,
                y=start_y + i * line_height
            )
            self.image.blit(text_surface, text_rect)
