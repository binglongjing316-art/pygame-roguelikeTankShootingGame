import pygame

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 880
# 系统检测
OS_SYSTEM = None
# 游戏全局设置
FPS = 60  # 帧率
# 颜色常量定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (80, 80, 80)

# 游戏常数参数设置
KEY_MOVE_ACCELERATION = 0.1  # 键盘移动加速度

# 网格系统
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # 40列
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # 22行
grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]  # 40x22网格

# 游戏窗口设置
game_is_fullscreen = False
screen_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).get_rect()
pygame.display.set_caption("坦克大战")
screen = pygame.display.set_mode((800, 440), pygame.RESIZABLE)  # 默认展示窗口大小
# 虚拟屏幕
virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


# 加载音效
def init_sounds():
    """
    初始化游戏音效
    """
    global hit_sound, shooting_sound, death_sound, game_over_sound, bgm
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.set_num_channels(128)  # 设置为128个通道
    pygame.time.delay(1000)  # 等待1秒以确保音频系统初始化完成
    hit_sound = pygame.mixer.Sound('sound/hit.wav')
    hit_sound.set_volume(1)
    shooting_sound = pygame.mixer.Sound('sound/shooting.wav')
    shooting_sound.set_volume(0.4)
    death_sound = pygame.mixer.Sound('sound/death.wav')
    game_over_sound = pygame.mixer.Sound('sound/gameover.wav')
    bgm = pygame.mixer.Sound('sound/bgm.wav')


global hit_sound, shooting_sound, death_sound, game_over_sound, bgm
