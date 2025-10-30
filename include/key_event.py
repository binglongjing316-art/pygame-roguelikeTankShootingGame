import math

import pygame

from include import variable, constant, buttons, console
from include import card as include_card

from include import prop_functions
from include.restart import restart
from include.sprites_init import players, Texts, booms
from spirit.functionCard import FunctionCard

# 按键的总事件
event_type = {
    "menu":
        {
            pygame.K_ESCAPE: "exit",
            # 事件类型
            pygame.K_SPACE: "restart",
            pygame.K_RETURN: "restart"
        },
    "game_pause":
        {
            pygame.K_p: "continue",
            pygame.K_1: "select_1",
            pygame.K_2: "select_2",
            pygame.K_3: "select_3",
            pygame.K_z: "delete_card",
            pygame.K_ESCAPE: "menu"
        },
    "game_over":
        {
            pygame.K_r: "restart",
            pygame.K_ESCAPE: "menu"
        },
    "game_start":
        {
            pygame.K_p: "pause",
            pygame.K_ESCAPE: "menu",
            pygame.K_q: "select_card",
            pygame.K_SPACE: "use_prop",
            pygame.K_BACKQUOTE: "console_open"
        },
    "console":
        {
            # 按键类型
            pygame.K_BACKQUOTE: "console_close",
            pygame.K_RETURN: "console_execute",
            pygame.K_BACKSPACE: "console_backspace",
            pygame.K_UP: "console_up",
            pygame.K_DOWN: "console_down",
            pygame.K_ESCAPE: "console_close",
            # 事件类型
            pygame.TEXTINPUT: "console_input_text",
        }
}


def get_button_event_type(event):
    # 转换鼠标坐标到虚拟屏幕
    mouse_pos = pygame.mouse.get_pos()
    scale_x = constant.screen.get_width() / constant.SCREEN_WIDTH
    scale_y = constant.screen.get_height() / constant.SCREEN_HEIGHT
    scale = min(scale_x, scale_y)
    scaled_width = int(constant.SCREEN_WIDTH * scale)
    scaled_height = int(constant.SCREEN_HEIGHT * scale)
    offset_x = (constant.screen.get_width() - scaled_width) // 2
    offset_y = (constant.screen.get_height() - scaled_height) // 2
    virtual_mouse_x = (mouse_pos[0] - offset_x) / scale
    virtual_mouse_y = (mouse_pos[1] - offset_y) / scale
    if variable.game_state == "game_pause":
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检测删卡按钮
                if buttons.del_btn_rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                    return "delete_card"
                # 点击选卡
                for functionCard in Texts:  # 检查所有的文字组
                    # 如果是卡片类型，并且点击了卡片
                    if isinstance(functionCard, FunctionCard) \
                            and functionCard.rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                        if functionCard.index == 0:
                            return "select_1"
                        elif functionCard.index == 1:
                            return "select_2"
                        elif functionCard.index == 2:
                            return "select_3"
                # 检测继续按钮
                if buttons.restart_btn_rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                    return "continue"
    elif variable.game_state == "game_over":
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检测重新开始按钮
                if buttons.restart_btn_rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                    return "restart"
    elif variable.game_state == "game_start":
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检测选卡按钮
                if buttons.card_btn_rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                    return "select_card"
                # 检测重新开始按钮
                if buttons.restart_btn_rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                    return "pause"
                # 检测道具
                if buttons.prop_btn_rect.collidepoint(virtual_mouse_x, virtual_mouse_y):
                    return "use_prop"
    elif variable.game_state == "menu":
        if event.type == pygame.MOUSEBUTTONDOWN:
            restart()


def handle_key_events(event):
    player = None
    for player in players:
        pass
    action = None
    if event.type == pygame.MOUSEBUTTONDOWN:
        action = get_button_event_type(event)
    elif event.type == pygame.KEYDOWN:
        action = event_type.get(variable.game_state, {}).get(event.key, None)
    else:
        # 其他类型
        action = event_type.get(variable.game_state, {}).get(event.type, None)
    if action == "continue":
        if not variable.is_choosing_card:
            variable.game_state = "game_start"
    elif action == "pause":
        variable.game_state = "game_pause"
    elif action == "menu":
        variable.game_state = "menu"
    elif action == "select_card":
        if variable.can_card_choose_number > 0 and not variable.is_choosing_card:
            variable.card_choose_key_pressed = True
    elif action == "delete_card":
        if variable.can_card_choose_number > 0 and variable.is_choosing_card:
            player.health += player.health_max * 0.1
            if player.health > player.health_max:
                player.health = player.health_max
            # 清除卡片
            for c in Texts:
                if isinstance(c, FunctionCard):
                    c.kill()
            variable.can_card_choose_number -= 1
            variable.is_choosing_card = False
            if variable.can_card_choose_number == 0:
                variable.game_state = "game_start"
                variable.card_choose_key_pressed = False
    elif action == "use_prop":
        if len(player.prop_list) >= 1:
            prop_functions.prop_function(player.prop_list[-1], player)
    elif action == "select_1" or action == "select_2" or action == "select_3":
        for functionCard in Texts:
            if action == "select_1":
                card_index = 0
            elif action == "select_2":
                card_index = 1
            elif action == "select_3":
                card_index = 2
            else:
                card_index = 0
            # 卡片序号与选择卡片序号相同，则应用卡片效果
            if isinstance(functionCard, FunctionCard) and functionCard.index == card_index:
                include_card.card_function(functionCard.function)
                # 清除卡片
                for c in Texts:
                    if isinstance(c, FunctionCard):
                        c.kill()
                variable.can_card_choose_number -= 1
                variable.is_choosing_card = False
                if variable.can_card_choose_number == 0:
                    variable.game_state = "game_start"
                    variable.card_choose_key_pressed = False
    elif action == "console_open":
        variable.game_state = "console"
    elif action == "console_close":
        variable.game_state = "game_start"
    elif action == "console_execute":
        console.console_execute()
    elif action == "console_backspace":
        console.console_backspace()
    elif action == "console_up":
        console.console_input_up()
    elif action == "console_down":
        console.console_input_down()
    elif action == "restart":
        constant.game_over_sound.stop()
        restart()
    elif action == "exit":
        variable.running = False
    elif action == "console_input_text":
        if event.text != '`':
            console.console_input_text(event.text)

    # (手机测试用)
    if event.type == pygame.FINGERDOWN and (constant.OS_SYSTEM == 'Android' or constant.OS_SYSTEM == 'iOS'):
        # 转换为虚拟屏幕坐标
        scale_x = constant.screen.get_width() / constant.SCREEN_WIDTH
        scale_y = constant.screen.get_height() / constant.SCREEN_HEIGHT
        scale = min(scale_x, scale_y)
        offset_x = (constant.screen.get_width() - constant.SCREEN_WIDTH * scale) // 2
        offset_y = (constant.screen.get_height() - constant.SCREEN_HEIGHT * scale) // 2
        virtual_x = (event.x * constant.screen.get_width() - offset_x) / scale
        virtual_y = (event.y * constant.screen.get_height() - offset_y) / scale
        finger_id = event.finger_id
        # 先检测移动摇杆区域
        dx = virtual_x - buttons.move_joystick_pos[0]
        dy = virtual_y - buttons.move_joystick_pos[1]
        if math.hypot(dx, dy) < buttons.JOYSTICK_RADIUS * 2:  # 扩大感应范围
            buttons.touch_points[finger_id] = {
                "type": "move",
                "start_pos": (virtual_x, virtual_y),
                "current_pos": (virtual_x, virtual_y)
            }
        else:
            # 检测射击按钮
            for btn in buttons.shoot_btns:
                if btn['rect'].collidepoint(virtual_x, virtual_y):
                    buttons.touch_points[finger_id] = {
                        "type": "shoot",
                        "dir": btn['dir'],
                        "current_pos": (virtual_x, virtual_y)
                    }
                    break
    elif event.type == pygame.FINGERMOTION and (constant.OS_SYSTEM == 'Android' or constant.OS_SYSTEM == 'iOS'):
        finger_id = event.finger_id
        if finger_id in buttons.touch_points:
            # 更新坐标
            scale_x = constant.screen.get_width() / constant.SCREEN_WIDTH
            scale_y = constant.screen.get_height() / constant.SCREEN_HEIGHT
            scale = min(scale_x, scale_y)
            offset_x = (constant.screen.get_width() - constant.SCREEN_WIDTH * scale) // 2
            offset_y = (constant.screen.get_height() - constant.SCREEN_HEIGHT * scale) // 2
            virtual_x = (event.x * constant.screen.get_width() - offset_x) / scale
            virtual_y = (event.y * constant.screen.get_height() - offset_y) / scale
            buttons.touch_points[finger_id]["current_pos"] = (virtual_x, virtual_y)
    elif event.type == pygame.FINGERUP and (constant.OS_SYSTEM == 'Android' or constant.OS_SYSTEM == 'iOS'):
        finger_id = event.finger_id
        if finger_id in buttons.touch_points:
            del buttons.touch_points[finger_id]


def handle_repeat_events():
    player = None
    for player in players:
        pass
    # （手机测试用）
    if constant.OS_SYSTEM == 'Android' or constant.OS_SYSTEM == 'iOS':
        # 移动摇杆处理
        move_inputs = []
        for tp in buttons.touch_points.values():
            if tp["type"] == "move":
                # 计算相对偏移
                dx = tp["current_pos"][0] - tp["start_pos"][0]
                dy = tp["current_pos"][1] - tp["start_pos"][1]
                distance = math.hypot(dx, dy)

                # 限制在摇杆范围内
                if distance > buttons.JOYSTICK_RADIUS:
                    dx = dx * buttons.JOYSTICK_RADIUS / distance
                    dy = dy * buttons.JOYSTICK_RADIUS / distance

                # 转换为方向向量
                norm_dx = dx / buttons.JOYSTICK_RADIUS
                norm_dy = dy / buttons.JOYSTICK_RADIUS
                move_inputs.append((norm_dx, norm_dy))
        # 计算平均输入
        if move_inputs:
            avg_dx = sum(i[0] for i in move_inputs) / len(move_inputs)
            avg_dy = sum(i[1] for i in move_inputs) / len(move_inputs)
            player.move(avg_dx, avg_dy)
        # 射击处理
        shoot_dirs = [tp["dir"] for tp in buttons.touch_points.values() if tp["type"] == "shoot"]
        if shoot_dirs and not player.is_shoot_cooling:
            # 取最后一个按下的射击方向
            player.shoot(shoot_dirs[-1])
            player.is_shoot_cooling = True
    # 键盘移动控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and not keys[pygame.K_d]:
        variable.move_dx -= constant.KEY_MOVE_ACCELERATION
        if variable.move_dx < -1:
            variable.move_dx = -1
    elif variable.move_dx < 0:
        variable.move_dx += constant.KEY_MOVE_ACCELERATION
        if variable.move_dx > 0:
            variable.move_dx = 0
    if keys[pygame.K_d] and not keys[pygame.K_a]:
        variable.move_dx += constant.KEY_MOVE_ACCELERATION
        if variable.move_dx > 1:
            variable.move_dx = 1
    elif variable.move_dx > 0:
        variable.move_dx -= constant.KEY_MOVE_ACCELERATION
        if variable.move_dx < 0:
            variable.move_dx = 0
    if keys[pygame.K_w] and not keys[pygame.K_s]:
        variable.move_dy -= constant.KEY_MOVE_ACCELERATION
        if variable.move_dy < -1:
            variable.move_dy = -1
    elif variable.move_dy < 0:
        variable.move_dy += constant.KEY_MOVE_ACCELERATION
        if variable.move_dy > 0:
            variable.move_dy = 0
    if keys[pygame.K_s] and not keys[pygame.K_w]:
        variable.move_dy += constant.KEY_MOVE_ACCELERATION
        if variable.move_dy > 1:
            variable.move_dy = 1
    elif variable.move_dy > 0:
        variable.move_dy -= constant.KEY_MOVE_ACCELERATION
        if variable.move_dy < 0:
            variable.move_dy = 0
    player.move(variable.move_dx, variable.move_dy)
    # 键盘射击
    if player.is_shoot_cooling is False:
        if keys[pygame.K_UP]:
            player.shoot('up')
            player.is_shoot_cooling = True
        elif keys[pygame.K_DOWN]:
            player.shoot('down')
            player.is_shoot_cooling = True
        elif keys[pygame.K_LEFT]:
            player.shoot('left')
            player.is_shoot_cooling = True
        elif keys[pygame.K_RIGHT]:
            player.shoot('right')
            player.is_shoot_cooling = True
    else:
        player.shoot_cooling_count += 0.1
        if player.shoot_cooling_count >= player.shoot_cooling_count_max:
            player.shoot_cooling_count = 0
            player.is_shoot_cooling = False
    if len(player.prop_list) >= 1 and player.prop_list[-1] == "boom":
        if keys[pygame.K_UP]:
            for boom in booms:
                boom.direct = "up"
        elif keys[pygame.K_DOWN]:
            for boom in booms:
                boom.direct = "down"
        elif keys[pygame.K_LEFT]:
            for boom in booms:
                boom.direct = "left"
        elif keys[pygame.K_RIGHT]:
            for boom in booms:
                boom.direct = "right"
        else:
            for boom in booms:
                boom.direct = None
