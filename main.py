"""

"""
import time
import pygame
import random
import sys
from include import constant, variable, console, key_event, buttons
from include import card as include_card

from include import prop_functions
from include.restart import restart
from include.function import count_label_sprites
from include.sprites_init import all_sprites, enemies, walls, bullets, players, timers, Texts, booms

from spirit.floatingText import FloatingText
from spirit.functionCard import FunctionCard, _split_text
from spirit.tank import Tank
from spirit.timer import Timer
from spirit.wall import Wall

# 初始化Pygame库及音效模块
pygame.init()
constant.init_sounds()
constant.bgm.set_volume(0)
constant.OS_SYSTEM = pygame.display.get_driver()
# 游戏全局设置
clock = pygame.time.Clock()  # 游戏时钟(控制帧率)
start = time.time()

# 创建玩家坦克
player = Tank(label=['player'])
players.add(player)
all_sprites.add(player)
variable.game_state = "menu"

# 游戏主循环
while variable.running:
    # 控制游戏帧率
    clock.tick(constant.FPS)
    # 游戏事件处理循环
    for event in pygame.event.get():
        # 处理不同类型按键事件
        key_event.handle_key_events(event)
        if event.type == pygame.QUIT:  # 退出游戏
            variable.running = False
        elif event.type == pygame.VIDEORESIZE:  # 窗口尺寸变化时自动调整
            if not constant.game_is_fullscreen:  # 全屏时不处理
                constant.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN and variable.game_state != "console":
            # 全局键盘事件处理(优先级低于控制台)
            if event.key == pygame.K_EQUALS:  # 音量＋=
                constant.bgm.set_volume(constant.bgm.get_volume() + 0.1)
            elif event.key == pygame.K_MINUS:  # 音量--
                constant.bgm.set_volume(constant.bgm.get_volume() - 0.1)
                if constant.bgm.get_volume() < 0.1:
                    constant.bgm.set_volume(0)
            elif event.key == pygame.K_f:  # 切换全屏
                if constant.game_is_fullscreen:
                    constant.game_is_fullscreen = False
                    constant.screen = pygame.display.set_mode((800, 440), pygame.RESIZABLE)
                else:
                    constant.game_is_fullscreen = True
                    constant.screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT),
                                                              pygame.FULLSCREEN)
    variable.index_global += 1
    # 升级
    while variable.score > player.level_up_score_limit:
        player.level_up_score_limit += 20 + player.level ** 1.5
        player.level += 1
        ratio = player.health / player.health_max
        player.health_max += 10
        player.damage_initial += 1
        player.health = int(float(player.health_max) * ratio)
        #  卡牌获取限制
        if player.level < 20:
            card_choose_interval = 2
        elif player.level < 40:
            card_choose_interval = 3
        elif player.level < 60:
            card_choose_interval = 4
        elif player.level < 80:
            card_choose_interval = 5
        elif player.level < 100:
            card_choose_interval = 5
        else:
            card_choose_interval = 5
        if player.level % card_choose_interval == 0:
            variable.can_card_choose_number += 1
    # 触发选卡
    if variable.can_card_choose_number > 0 and not variable.is_choosing_card and variable.card_choose_key_pressed:
        variable.game_state = "game_pause"
        variable.is_choosing_card = True
        re_choose = [True, True, True]
        while re_choose[0] or re_choose[1] or re_choose[2]:
            include_card.card_options = random.sample(include_card.card_functions, 3)
            for i, func in enumerate(include_card.card_options):
                if random.uniform(1, 100) < func["redrawProb"]:  # 逆权重， 重新选择的概率
                    re_choose[i] = True
                else:
                    re_choose[i] = False
        for i, func in enumerate(include_card.card_options):
            # 生成卡片
            card = FunctionCard(i, func)
            all_sprites.add(card)
            Texts.add(card)  # 用Texts组显示卡片

    # 游戏主循环
    if variable.game_state == "game_start":
        # 游戏计数增加
        variable.index += 1
        # 移动控制函数
        key_event.handle_repeat_events()  # 处理重复事件
        # 墙体被击中的逻辑
        for wall in walls:
            hits = pygame.sprite.spritecollide(wall, bullets, False)  # 改为False
            for bullet in hits:
                if bullet.penetrate:
                    pass
                else:
                    bullet.kill()  # 非穿透子弹移除
                # 检查是否已命中过该墙体
                if wall not in bullet.hit_targets:
                    wall.health -= bullet.damage
                    if 'player' in bullet.label:
                        if "penetrate" in player.card_functions_list or "borer" in player.card_functions_list:
                            pass
                        else:
                            constant.hit_sound.play()  # 击中音效
                    if bullet.penetrate:
                        bullet.hit_targets.add(wall)  # 记录已经击中过的对象

        # 敌方被击中的逻辑
        player_bullets = pygame.sprite.Group()
        for bullet in bullets:
            if 'player' in bullet.label:
                player_bullets.add(bullet)
        for enemy in enemies:
            hits = pygame.sprite.spritecollide(enemy, player_bullets, False)
            for bullet in hits:
                # 穿透子弹专属逻辑
                if bullet.penetrate:
                    pass
                else:
                    bullet.kill()  # 非穿透子弹移除
                # 检查是否已命中过该敌人
                if enemy not in bullet.hit_targets:
                    enemy.health -= bullet.damage
                    if bullet.penetrate:
                        borer = False
                        if "borer" in player.card_functions_list:
                            borer = True
                        if not borer:
                            bullet.hit_targets.add(enemy)  # 记录已经击中过的对象
                    constant.hit_sound.play()  # 击中音效
                    # 吸血效果
                    player.health += bullet.damage * player.leech_rate
                    # 吸血数字生成
                    if bullet.damage * player.leech_rate >= 1:
                        cure_text = FloatingText(
                            player.rect.right + 10,  # 右侧偏移
                            player.rect.top - 10,  # 顶部上方
                            bullet.damage * player.leech_rate,
                            (0, 255, 0)
                        )
                        Texts.add(cure_text)
                    # 伤害数字生成
                    damage_text = FloatingText(
                        enemy.rect.right + 10,  # 右侧偏移
                        enemy.rect.top - 10,  # 顶部上方
                        bullet.damage,
                        (255, 50, 50)  # 更醒目的红色
                    )
                    Texts.add(damage_text)

        # 玩家被击中的逻辑
        enemy_bullets = pygame.sprite.Group()
        for bullet in bullets:
            if 'enemy' in bullet.label:
                enemy_bullets.add(bullet)
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            constant.hit_sound.play()
            for bullet in hits:
                player.health -= bullet.damage
                # 伤害数字生成
                damage_text = FloatingText(
                    player.rect.right + 10,  # 右侧偏移
                    player.rect.top - 10,  # 顶部上方
                    bullet.damage,
                    constant.RED
                )
                Texts.add(damage_text)

        # 所有计时器到期事件
        for timer in timers:
            if timer.is_expire:
                # 新敌人生成计时器到期
                if timer.label == 'new_enemy_spawn_timer':
                    # 新敌人增加
                    if len(enemies) >= 30:  # 敌人上限
                        pass
                    else:
                        if variable.score >= 300:
                            new_enemy = Tank(label=['enemy'])
                            new_enemy.health = player.level * 10
                            new_enemy.health_max = player.level * 10
                            new_enemy.score_level = new_enemy.health // 3
                            new_enemy.damage_initial = player.level * 2 if player.level * 2 > 20 else 20
                            all_sprites.add(new_enemy)
                            enemies.add(new_enemy)
                        else:
                            new_enemy = Tank(label=['enemy'])
                            all_sprites.add(new_enemy)
                            enemies.add(new_enemy)
                    # 不同敌人增加
                    variable.enemy_killed_count += 1
                    if variable.enemy_killed_count % 6 == 0:
                        new_enemy = Tank(label=['enemy', 'sniper'])
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)
                    if variable.enemy_killed_count % 3 == 0:
                        new_enemy = Tank(label=['enemy', 'chaser'])
                        all_sprites.add(new_enemy)
                        enemies.add(new_enemy)
                # Boss生成计时器到期
                elif timer.label == 'boss_spawn_timer':
                    if count_label_sprites(enemies, 'boss') == 0:
                        boss = Tank(label=['boss', 'boss1', 'enemy'])  # 橙色Boss
                        boss.health = 200000
                        boss.health_max = 200000
                        boss.damage_initial = 450
                        boss.random_damage_range = 100
                        boss.speed = 2
                        boss.score_level = 100000
                        all_sprites.add(boss)
                        enemies.add(boss)
                # 墙体重生计时器到期
                elif timer.label.startswith("wall_respawn"):
                    # 解析原始坐标
                    (x, y) = timer.label.split("_")[2], timer.label.split("_")[3]
                    x = int(x)
                    y = int(y)
                    # 检查重生条件
                    temp_wall = Wall(x, y)
                    temp_wall.rect.topleft = (x, y)
                    # 条件1: 不与现有墙体重叠
                    wall_collision = pygame.sprite.spritecollideany(temp_wall, walls)
                    # 条件2: 不与敌人玩家重叠
                    enemy_collision = pygame.sprite.spritecollideany(temp_wall, enemies)
                    player_collision = pygame.sprite.spritecollideany(temp_wall, players)
                    # 条件3: 不靠近玩家（距离>100像素）
                    dx = player.rect.x - x
                    dy = player.rect.y - y
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    if not wall_collision \
                            and not enemy_collision \
                            and distance > 100 \
                            and count_label_sprites(enemies, 'boss') == 0:
                        # 创建新墙体并设置血量
                        new_wall = Wall(x, y)
                        new_wall.health_max = player.damage_initial * 3
                        new_wall.health = new_wall.health_max
                        walls.add(new_wall)
                        all_sprites.add(new_wall)
                    else:
                        # 重新启动计时器
                        new_timer = Timer(20, timer.label)
                        timers.add(new_timer)

                timer.kill()  # 清除计时器
        # 更新所有游戏内精灵状态
        all_sprites.update()
        timers.update()
        booms.update()

    # 画面绘制(图层不同)
    constant.virtual_screen.fill(constant.BLACK)
    if variable.game_state == "game_start" or variable.game_state == "game_pause" \
            or variable.game_state == "game_over" or variable.game_state == "console":
        # 全局精灵更新
        Texts.update()

        # 炸弹绘制
        booms.draw(constant.virtual_screen)
        # 所有非重叠精灵绘制
        all_sprites.draw(constant.virtual_screen)

        # 绘制所有坦克的血条
        for tank in players.sprites() + enemies.sprites():
            if 'boss' in tank.label:
                bar_width = constant.SCREEN_WIDTH // 1.5  # 血条宽度
                bar_height = 8
                # 血条位置
                bar_x = constant.SCREEN_WIDTH // 2 - bar_width // 2
                bar_y = constant.SCREEN_HEIGHT // 15
                # 绘制血条背景（剩余血量）
                pygame.draw.rect(constant.virtual_screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
                # 绘制当前血量
                health_width = bar_width * (tank.health / tank.health_max)
                pygame.draw.rect(constant.virtual_screen, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
            else:
                if 0 < tank.health < tank.health_max:
                    # 血条位置（坦克顶部中央）
                    bar_width = tank.rect.width  # 血条宽度
                    bar_height = 5
                    # 计算血条位置
                    bar_x = tank.rect.centerx - bar_width // 2
                    bar_y = tank.rect.top - 10  # 坦克上方10像素
                    # 绘制血条背景（剩余血量）
                    pygame.draw.rect(constant.virtual_screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                    # 绘制当前血量（绿色部分）
                    health_width = bar_width * (tank.health / tank.health_max)
                    pygame.draw.rect(constant.virtual_screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        # 绘制道具条
        if len(player.prop_list) >= 1 and player.prop_cooling_max != 0:
            bar_width = 80
            bar_height = 10
            bar_color = (0, 255, 0) if player.prop_cooling_count == player.prop_cooling_max else (155, 155, 155)
            # 绘制道具条背景
            pygame.draw.rect(constant.virtual_screen, (20, 20, 100),
                             (50, constant.SCREEN_HEIGHT - 50, bar_width, bar_height))
            # 绘制道具条
            prop_width = player.prop_cooling_count / player.prop_cooling_max * bar_width
            pygame.draw.rect(constant.virtual_screen, bar_color,
                             (50, constant.SCREEN_HEIGHT - 50, prop_width, bar_height))
            # 绘制道具
            prop_functions.prop_show(player.prop_list[-1])

        # 文字组绘制
        Texts.draw(constant.virtual_screen)
        # 分数显示
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {variable.score}", True, constant.BLACK)
        constant.virtual_screen.blit(text, (11, 11))
        text = font.render(f"Score: {variable.score}", True, constant.WHITE)
        constant.virtual_screen.blit(text, (10, 10))
        # 生命值显示
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {round(player.health)}/{round(player.health_max)}", True, constant.BLACK)
        constant.virtual_screen.blit(health_text, (11, 91))
        health_text = font.render(f"Health: {round(player.health)}/{round(player.health_max)}", True, constant.GREEN)
        constant.virtual_screen.blit(health_text, (10, 90))
        # 等级显示
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {player.level}", True, constant.BLACK)
        constant.virtual_screen.blit(level_text, (11, 51))
        level_text = font.render(f"Level: {player.level}", True, constant.WHITE)
        constant.virtual_screen.blit(level_text, (10, 50))

        # 绘制所有按钮
        buttons.draw_all_button()

    # 游戏结束画面
    if variable.game_state == "game_over":
        variable.can_card_choose_number = 0
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER! Press R to restart", True, constant.RED)
        constant.virtual_screen.blit(text, (constant.SCREEN_WIDTH // 2 - 180, constant.SCREEN_HEIGHT // 2))
    # 游戏暂停画面
    if variable.game_state == "game_pause":
        font = pygame.font.Font(None, 50)
        text = font.render("GAME SUSPENDED", True, constant.BLACK)
        constant.virtual_screen.blit(text, (constant.SCREEN_WIDTH // 2 - 182, (constant.SCREEN_HEIGHT // 6) + 2))
        font = pygame.font.Font(None, 50)
        text = font.render("GAME SUSPENDED", True, constant.WHITE)
        constant.virtual_screen.blit(text, (constant.SCREEN_WIDTH // 2 - 180, constant.SCREEN_HEIGHT // 6))
        # 玩家数值显示
        font = pygame.font.Font(None, 36)
        attributes = [
            ('Speed', player.speed, player.init_speed, '{:.2f}'),
            ('Shoot Speed', player.shoot_speed * player.shoot_speed_multiplier, player.init_shoot_speed, '{:.2f}'),
            ('Bullet Speed', player.bullet_speed, player.init_bullet_speed, '{:.2f}'),
            ('Damage', player.damage_initial * player.damage_multiplier, player.init_damage_initial, '{:.2f}'),
            ('Leech Rate', player.leech_rate * 100, player.init_leech_rate, '{:.2f}%'),
            ('Crit Chance', player.critical_chance, player.init_critical_chance, '{:.2f}%'),
            ('Crit Damage', player.critical_damage, player.init_critical_damage, '{:.2f}%'),
            ('Range', player.range, player.init_range, '{:.0f}'),
            ('Card', ', '.join(player.card_functions_list), '', '{}'),
            ('Prop', ', '.join(player.prop_list), '', '{}'),
            ('test', str([player.damage_multiplier, player.shoot_speed_multiplier]), '', '{}')
        ]
        y_start = 130
        for i, (label, value, init_value, fmt) in enumerate(attributes):
            text_value = fmt.format(value)
            if (label == "Card" or label == "Prop") and value == "":
                text_value = 'empty'
            if init_value > value:
                c = constant.RED
            elif init_value < value:
                c = constant.GREEN
            else:
                c = constant.WHITE
            text = font.render(f"{label}: {text_value}", True, constant.BLACK)
            constant.virtual_screen.blit(text, (12, y_start + i * 30 + 2))
            text = font.render(f"{label}: {text_value}", True, c)
            constant.virtual_screen.blit(text, (10, y_start + i * 30))
    # 绘制控制台界面
    if variable.game_state == "console":
        # 半透明背景
        console_surf = pygame.Surface((constant.SCREEN_WIDTH, console.console_surf_h), pygame.SRCALPHA)
        console_surf.fill((30, 30, 30, 200))  # 深灰色半透明
        constant.virtual_screen.blit(console_surf, (0, constant.SCREEN_HEIGHT - console.console_surf_h))
        # 文本
        txt_height = console.console_font.render("> ", True, constant.WHITE).get_height()
        if variable.index_global % 60 > 30:
            input_text = console.console_font.render("> " + console.console_input + "_", True, constant.WHITE)
        else:
            input_text = console.console_font.render("> " + console.console_input, True, constant.WHITE)
        if console.console_output[1] == "error":
            output_text = console.console_font.render("> " + console.console_output[0], True, constant.RED)
        elif console.console_output[1] == "success":
            output_text = console.console_font.render("> " + console.console_output[0], True, constant.GREEN)
        else:
            output_text = console.console_font.render("> " + console.console_output[0], True, constant.WHITE)

        hint_text = console.console_font.render(console.console_hint, True, constant.GRAY)
        # 绘制文本
        if hint_text.get_width() > constant.SCREEN_WIDTH - 100:
            for i, line in enumerate(
                    _split_text(console.console_font, console.console_hint, constant.SCREEN_WIDTH - 100, "       ")):
                hint_text = console.console_font.render(line, True, constant.GRAY)
                constant.virtual_screen.blit(hint_text,
                                             (10, constant.SCREEN_HEIGHT - console.console_surf_h + 10 + txt_height * (
                                                     2 + i)))
        else:
            constant.virtual_screen.blit(hint_text,
                                         (10, constant.SCREEN_HEIGHT - console.console_surf_h + 10 + txt_height * 2))
        constant.virtual_screen.blit(input_text, (10, constant.SCREEN_HEIGHT - console.console_surf_h + 10))
        constant.virtual_screen.blit(output_text,
                                     (10, constant.SCREEN_HEIGHT - console.console_surf_h + 10 + txt_height))
    # 游戏主菜单画面
    if variable.game_state == "menu":
        # 显示游戏标题
        title_font = pygame.font.Font(None, 96)
        title_text = title_font.render("Roguelike Battle", True, constant.WHITE)
        constant.virtual_screen.blit(title_text, (
            constant.SCREEN_WIDTH // 2 - title_text.get_width() // 2, constant.SCREEN_HEIGHT // 4))
        if variable.index_global % 60 < 30:
            # 显示开始提示
            hint_font = pygame.font.Font(None, 36)
            hint_text = hint_font.render("Press space to start", True, constant.GRAY)
            constant.virtual_screen.blit(hint_text, (
                constant.SCREEN_WIDTH // 2 - hint_text.get_width() // 2, constant.SCREEN_HEIGHT // 2))

        # 显示版本或作者信息（可选）
        info_font = pygame.font.Font(None, 24)
        info_text = info_font.render("Developed by ice dc", True, constant.DARK_GRAY)
        constant.virtual_screen.blit(info_text, (
            constant.SCREEN_WIDTH // 2 - info_text.get_width() // 2, constant.SCREEN_HEIGHT - 50))
    # 帧率显示
    variable.fps_count += 1
    now = time.time()
    fps = '{0:.2f}'.format(variable.fps_count / (now - start))
    if variable.fps_count == 125:  # 每125帧重新计算
        variable.fps_count = 0
        start = time.time()
    font = pygame.font.Font(None, 30)
    FPStext = font.render(str(fps), True, constant.RED)
    constant.virtual_screen.blit(FPStext, (constant.SCREEN_WIDTH - 100, 25))
    # 计算缩放比例
    scale_x = constant.screen.get_width() / constant.SCREEN_WIDTH
    scale_y = constant.screen.get_height() / constant.SCREEN_HEIGHT
    scale = min(scale_x, scale_y)  # 保持宽高比
    # 缩放虚拟屏幕并居中显示
    scaled_surf = pygame.transform.scale(constant.virtual_screen,
                                         (int(constant.SCREEN_WIDTH * scale), int(constant.SCREEN_HEIGHT * scale)))
    constant.screen.blit(scaled_surf, (
        (constant.screen.get_width() - scaled_surf.get_width()) // 2,
        (constant.screen.get_height() - scaled_surf.get_height()) // 2
    ))
    # 更新显示
    pygame.display.flip()

# 退出游戏
pygame.quit()
sys.exit()
