# 界面按钮设置
import math

import pygame

from include import constant, variable

# 触摸跟踪字典(手机测试用)
touch_points = {}  # 结构：{finger_id: {"type": "move/shoot", "pos": (x,y)}}
BUTTON_ALPHA = 150  # 按钮透明度
JOYSTICK_RADIUS = 100  # 摇杆半径
BUTTON_SIZE = 80 if constant.OS_SYSTEM == "windows" else 150 if constant.OS_SYSTEM == 'Android' or constant.OS_SYSTEM == 'iOS' else 80  # 功能按钮尺寸
# 移动摇杆参数(手机测试用)
move_joystick_pos = (JOYSTICK_RADIUS + JOYSTICK_RADIUS, constant.SCREEN_HEIGHT - JOYSTICK_RADIUS - JOYSTICK_RADIUS)
# 射击按钮参数(手机测试用)
shoot_btns = [
    {'rect': pygame.Rect(constant.SCREEN_WIDTH - 2 * BUTTON_SIZE, constant.SCREEN_HEIGHT - 3 * BUTTON_SIZE, BUTTON_SIZE,
                         BUTTON_SIZE),
     'dir': 'up'},
    {'rect': pygame.Rect(constant.SCREEN_WIDTH - 1 * BUTTON_SIZE, constant.SCREEN_HEIGHT - 2 * BUTTON_SIZE, BUTTON_SIZE,
                         BUTTON_SIZE),
     'dir': 'right'},
    {'rect': pygame.Rect(constant.SCREEN_WIDTH - 2 * BUTTON_SIZE, constant.SCREEN_HEIGHT - 1 * BUTTON_SIZE, BUTTON_SIZE,
                         BUTTON_SIZE),
     'dir': 'down'},
    {'rect': pygame.Rect(constant.SCREEN_WIDTH - 3 * BUTTON_SIZE, constant.SCREEN_HEIGHT - 2 * BUTTON_SIZE, BUTTON_SIZE,
                         BUTTON_SIZE),
     'dir': 'left'}
]
# 选卡按钮
card_btn_rect = pygame.Rect(constant.SCREEN_WIDTH - 1.5 * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)
# 删卡按钮
del_btn_rect = pygame.Rect(constant.SCREEN_WIDTH - 1.5 * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)
# 重新开始或暂停按钮
restart_btn_rect = pygame.Rect(constant.SCREEN_WIDTH - BUTTON_SIZE, BUTTON_SIZE // 5, BUTTON_SIZE, BUTTON_SIZE)
# 道具按钮
prop_btn_rect = pygame.Rect(90 - BUTTON_SIZE // 2, constant.SCREEN_HEIGHT - 60 - BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)


def draw_all_button():
    # 游戏开始和暂停状态下绘制按钮
    if variable.game_state == "game_start" or variable.game_state == "game_pause":
        # 绘制控制界面
        # （手机测试用）
        if constant.OS_SYSTEM == 'Android' or constant.OS_SYSTEM == 'iOS':
            # 绘制基础摇杆
            joystick_surf = pygame.Surface((JOYSTICK_RADIUS * 4, JOYSTICK_RADIUS * 4), pygame.SRCALPHA)
            alf = BUTTON_ALPHA // 5
            for tp in touch_points.values():
                if tp["type"] == "move":
                    alf = BUTTON_ALPHA
            pygame.draw.circle(joystick_surf, (*constant.WHITE, alf),
                               (JOYSTICK_RADIUS * 2, JOYSTICK_RADIUS * 2), JOYSTICK_RADIUS)
            # 绘制所有活动摇杆点
            for tp in touch_points.values():
                if tp["type"] == "move":
                    dx = tp["current_pos"][0] - tp["start_pos"][0]
                    dy = tp["current_pos"][1] - tp["start_pos"][1]
                    distance = math.hypot(dx, dy)
                    if distance > JOYSTICK_RADIUS:
                        dx = dx * JOYSTICK_RADIUS / distance
                        dy = dy * JOYSTICK_RADIUS / distance
                    pygame.draw.circle(joystick_surf, (*constant.WHITE, 200),
                                       (JOYSTICK_RADIUS * 2 + dx, JOYSTICK_RADIUS * 2 + dy), 20)
            constant.virtual_screen.blit(joystick_surf,
                                         (move_joystick_pos[0] - JOYSTICK_RADIUS * 2,
                                          move_joystick_pos[1] - JOYSTICK_RADIUS * 2))
            # 射击按钮
            shoot_surf = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
            shoot_dirs = [tp["dir"] for tp in touch_points.values() if tp["type"] == "shoot"]
            for btn in shoot_btns:
                btn_color = (*constant.WHITE, BUTTON_ALPHA) if btn['dir'] in shoot_dirs else (
                    *constant.WHITE, BUTTON_ALPHA // 2)
                pygame.draw.circle(shoot_surf, btn_color, (BUTTON_SIZE // 2, BUTTON_SIZE // 2), BUTTON_SIZE // 2)
                # 绘制方向箭头
                arrow_size = 20
                if btn['dir'] == 'up':
                    points = [(BUTTON_SIZE // 2, 10), (BUTTON_SIZE // 2 - arrow_size, 30),
                              (BUTTON_SIZE // 2 + arrow_size, 30)]
                elif btn['dir'] == 'down':
                    points = [(BUTTON_SIZE // 2, BUTTON_SIZE - 10), (BUTTON_SIZE // 2 - arrow_size, BUTTON_SIZE - 30),
                              (BUTTON_SIZE // 2 + arrow_size, BUTTON_SIZE - 30)]
                elif btn['dir'] == 'left':
                    points = [(10, BUTTON_SIZE // 2), (30, BUTTON_SIZE // 2 - arrow_size),
                              (30, BUTTON_SIZE // 2 + arrow_size)]
                else:  # right
                    points = [(BUTTON_SIZE - 10, BUTTON_SIZE // 2), (BUTTON_SIZE - 30, BUTTON_SIZE // 2 - arrow_size),
                              (BUTTON_SIZE - 30, BUTTON_SIZE // 2 + arrow_size)]
                pygame.draw.polygon(shoot_surf, constant.WHITE, points)
                constant.virtual_screen.blit(shoot_surf, btn['rect'])
        # 卡片提示
        if variable.can_card_choose_number > 0:
            if not variable.is_choosing_card:
                # 选卡提示
                font = pygame.font.Font(None, 36)
                text = font.render(f"Press Q to choose card({variable.can_card_choose_number})", True, constant.GRAY)
                constant.virtual_screen.blit(text, (constant.SCREEN_WIDTH - text.get_width(), BUTTON_SIZE * 2))
                # 选卡按钮
                card_surf = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(card_surf, (*constant.YELLOW, 255), (BUTTON_SIZE // 2, BUTTON_SIZE // 2),
                                   BUTTON_SIZE // 2)
                font = pygame.font.Font(None, 36)
                text = font.render(f"{variable.can_card_choose_number}(Q)", True, constant.GRAY)
                card_surf.blit(text,
                               (BUTTON_SIZE // 2 - text.get_width() // 2, BUTTON_SIZE // 2 - text.get_height() // 2))
                constant.virtual_screen.blit(card_surf, card_btn_rect)
            else:
                # 剩余卡片数量显示
                font = pygame.font.Font(None, 80)
                text = font.render(f"{variable.can_card_choose_number}", True, constant.BLACK)
                constant.virtual_screen.blit(text,
                                             (constant.SCREEN_WIDTH - constant.SCREEN_WIDTH // 2 - 43,
                                              constant.SCREEN_HEIGHT // 4))
                font = pygame.font.Font(None, 80)
                text = font.render(f"{variable.can_card_choose_number}", True, constant.WHITE)
                constant.virtual_screen.blit(text, (
                    constant.SCREEN_WIDTH - constant.SCREEN_WIDTH // 2 - 43 + 2, constant.SCREEN_HEIGHT // 4))
                # 删卡提示
                font = pygame.font.Font(None, 36)
                text = font.render(f"Press Z to discard the cards and get 10% of health", True, constant.GRAY)
                constant.virtual_screen.blit(text, (constant.SCREEN_WIDTH - text.get_width(), BUTTON_SIZE * 2))
                # 删卡按钮
                del_surf = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(del_surf, (*constant.RED, 255), (BUTTON_SIZE // 2, BUTTON_SIZE // 2),
                                   BUTTON_SIZE // 2)
                font = pygame.font.Font(None, 36)
                text = font.render(f"Z", True, constant.WHITE)
                del_surf.blit(text,
                              (BUTTON_SIZE // 2 - text.get_width() // 2, BUTTON_SIZE // 2 - text.get_height() // 2))
                constant.virtual_screen.blit(del_surf, del_btn_rect)
    # 重新开始/暂停按钮
    size = BUTTON_SIZE // 2
    restart_surf = pygame.Surface((size, size))
    if variable.game_state == "game_pause" or variable.game_state == "game_over":
        pygame.draw.polygon(restart_surf, constant.GREEN, [(size, size // 2), (0, size), (0, 0)])
        constant.virtual_screen.blit(restart_surf, restart_btn_rect)
    elif variable.game_state == "game_start":
        pygame.draw.line(restart_surf, constant.GREEN, (0, 0), (0, size), size // 2)
        pygame.draw.line(restart_surf, constant.GREEN, (size, 0), (size, size), size // 2)
        constant.virtual_screen.blit(restart_surf, restart_btn_rect)
