import random
import copy
import pygame
from include import constant, card, variable

from include.sprites_init import enemies, bullets, walls, all_sprites, timers, players, booms
from spirit.tank import Tank
from spirit.wall import Wall


# 初始化和重新开始及数值调整
def restart():
    player = None
    for player in players:
        pass  # 获取玩家对象
    # 清除敌人和子弹
    for enemy in enemies:
        enemy.kill()
    for _bullet in bullets:
        _bullet.kill()
    # 清除炸弹
    for boom in booms:
        boom.kill()
    # 生成随机墙体
    for wall in walls:
        wall.kill()
    for _ in range(random.randint(50, 200)):
        while True:

            # 生成在有效网格范围内的坐标
            grid_x = random.randint(0, constant.GRID_WIDTH - 1)
            grid_y = random.randint(0, constant.GRID_HEIGHT - 1)
            x = grid_x * constant.GRID_SIZE  # 转换为实际坐标
            y = grid_y * constant.GRID_SIZE
            wall = Wall(x, y)
            # 确保不与其他物体重叠
            if not pygame.sprite.spritecollideany(wall, all_sprites) and constant.screen_rect.colliderect(wall.rect):
                walls.add(wall)
                all_sprites.add(wall)
                break
    # 停止并重新播放BGM
    constant.bgm.stop()
    constant.bgm.play(-1)  # 新增循环播放

    # 玩家数值重置
    player.respawn()
    player.health = 100
    player.health_max = 100
    player.level = 0
    player.level_up_score_limit = 50

    player.card_functions_list = []
    player.prop_list = []
    player.speed = player.init_speed
    player.bullet_speed = player.init_bullet_speed
    player.shoot_speed = player.init_shoot_speed
    player.range = player.init_range
    player.damage_initial = player.init_damage_initial
    player.damage_multiplier = player.init_damage_multiplier
    player.shoot_speed_multiplier = player.init_shoot_speed_multiplier
    player.leech_rate = player.init_leech_rate
    player.critical_chance = player.init_critical_chance
    player.critical_damage = player.init_critical_damage
    player.random_damage_range = 5

    # 计数重置
    variable.score = 0
    variable.enemy_killed_count = 0
    variable.can_card_choose_number = 0
    variable.index = 0
    for t in timers:  # 删除所有计时器
        t.kill()

    # 创建新敌人
    for _ in range(3):
        enemy = Tank(label=['enemy'])
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 重新开始游戏
    variable.game_state = "game_start"
    variable.boss1_dead = False
    all_sprites.update()
    card.card_functions = copy.deepcopy(card.card_functions_all)  # 当前可选功能卡列表
