import math
import random
import pygame
from heapq import heappush, heappop
from include import constant, variable, function

from include.sprites_init import all_sprites, enemies, walls, bullets, players, timers
from spirit.bullet import Bullet
from spirit.timer import Timer
from include.console import debug_mode

boss1_dead = False  # Boss1是否被击杀


class Tank(pygame.sprite.Sprite):
    """坦克基类，包含玩家和敌人的共同属性"""

    def __init__(self, label):
        """
        初始化坦克
        :param label: 坦克标记(列表)

        """
        super().__init__()
        self.label = label
        # 初始化坦克属性(默认)
        # 外观
        self.size = 40
        self.color = constant.WHITE
        # 移动方向
        self.direction = "up"  # 初始方向
        self.move_direction_dx = 0  # 坦克x移动方向
        self.move_direction_dy = 0  # 坦克y移动方向
        # 属于自己的子弹
        self.bullets = pygame.sprite.Group()  # 子弹容器
        # 冷却
        self.is_shoot_cooling = False  # 射击冷却
        self.shoot_cooling_count = 0  # 射击冷却计数
        self.shoot_cooling_count_max = 3  # 射击冷却最大值
        self.is_prop_cooling = False  # 道具冷却
        self.prop_cooling_count = 0  # 道具冷却计数
        self.prop_cooling_max = 0
        # 其他
        self.card_functions_list = []  # 拥有卡片功能列表
        self.prop_list = []  # 拥有道具列表
        self.ai_move_direction_stateX = 'stop'  # 敌人默认运动状态x
        self.ai_move_direction_stateY = 'stop'  # 敌人默认运动状态y
        self.level = 1  # 等级
        self.level_up_score_limit = 50  # 升级分数限制
        self.leech_rate = 0  # 玩家吸血效果
        self.path = []  # 敌人路径
        # 默认属性
        self.bullet_speed = 5  # 子弹速度
        self.random_damage_range = 5  # 坦克随机伤害范围
        self.critical_chance = 0  # 坦克暴击概率
        self.critical_damage = 150  # 坦克暴击伤害
        self.range = 100  # 射程
        self.health_max = 100  # 生命最大值
        self.damage_initial = 20  # 坦克初始伤害
        self.score_level = 20  # 默认被击杀得分
        self.speed = 1  # 移动速度
        self.shoot_speed = 1.0  # 射速
        self.damage_multiplier = 1  # 伤害修正
        self.shoot_speed_multiplier = 1  # 射速修正
        # 初始化坦克属性(特殊坦克设置)
        if "enemy" in self.label:
            if "sniper" in self.label:
                self.color = (255, 200, 0)
                self.range = 9999
                self.health_max = 150
                self.damage_initial = 50
                self.score_level = 50
                self.speed = 0.5
            elif "chaser" in self.label:
                self.color = (255, 0, 155)
                self.health_max = 50
                self.damage_initial = 40
                self.score_level = 50
                self.speed = 2
            elif "boss" in self.label:
                self.color = (255, 255, 0)
                self.range = 9999
                if "boss1" in self.label:
                    self.size = 80
            else:
                self.color = (255, 0, 0)
                self.range = 100
                self.health_max = 20
                self.damage_initial = 20
        elif "player" in self.label:
            # 玩家特殊设置
            self.size = 35
            self.color = constant.GREEN

        # 应用默认属性
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)  # 坦克颜色
        self.rect = self.image.get_rect()  # 获取矩形碰撞区域
        self.health = self.health_max  # 当前生命值
        self.damage = self.damage_initial  # 坦克伤害

        self.respawn()  # 初始重生

        # 总开局玩家数值设置
        self.init_speed = 4  # 初始速度
        self.init_shoot_speed = 1.0  # 初始射速
        self.init_damage_initial = 20  # 初始伤害
        self.init_leech_rate = 0  # 初始吸血效果
        self.init_critical_chance = 0  # 初始暴击概率
        self.init_critical_damage = 150  # 初始暴击伤害
        self.init_bullet_speed = 5  # 初始子弹速度
        self.init_range = 50  # 初始射程
        self.init_shoot_speed_multiplier = 1  # 初始射速修正
        self.init_damage_multiplier = 1  # 初始伤害修正

    def respawn(self):
        """坦克重生逻辑"""
        while True:
            respawn_control = []
            # 玩家出生在中心，敌人随机出生
            if "player" in self.label:
                self.rect.center = (constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 2)
                # 删除中心的墙体
                collision_walls = pygame.sprite.spritecollide(self, walls, True)
                if collision_walls:
                    for collision_wall in collision_walls:
                        collision_wall.kill()
            else:
                self.rect.x = random.randint(0, constant.SCREEN_WIDTH - self.size)
                self.rect.y = random.randint(0, constant.SCREEN_HEIGHT - self.size)

            # 重生条件(不在碰撞下重生)
            if not pygame.sprite.spritecollideany(self, walls):  # 不重叠墙
                respawn_control.append(1)
            else:
                if "boss" in self.label:  # 如果是Boss
                    hits = pygame.sprite.spritecollide(self, walls, True)
                    if hits:
                        for hit in hits:
                            hit.kill()
                    respawn_control.append(1)
                else:
                    respawn_control.append(0)
            if "enemy" in self.label:  # 敌人重生
                # 计算敌人到玩家的向量
                player = None
                for _ in players:
                    player = _  # 获取玩家对象
                Dx = player.rect.centerx - self.rect.centerx
                Dy = player.rect.centery - self.rect.centery
                distance = (Dx ** 2 + Dy ** 2) ** 0.5
                if distance > 100:  # 不靠近玩家
                    respawn_control.append(1)
                else:
                    respawn_control.append(0)
                enemies_collided = pygame.sprite.spritecollide(self, enemies, False)
                enemies_collided = [e for e in enemies_collided if e != self]
                if not enemies_collided:  # 不重叠其他敌人
                    respawn_control.append(1)
                else:
                    if "boss" in self.label:  # 如果是Boss
                        for collision_enemy in enemies_collided:
                            collision_enemy.kill()
                        respawn_control.append(1)
                    else:
                        respawn_control.append(0)
            else:  # 玩家重生
                break
            if all(respawn_control):
                break

    def find_path(self, target):
        """A*路径规划"""
        start = (self.rect.x // constant.GRID_SIZE, self.rect.y // constant.GRID_SIZE)
        # 计算起始点在网格中的坐标
        end = (target.rect.x // constant.GRID_SIZE, target.rect.y // constant.GRID_SIZE)

        # 方向向量（允许八方向移动）
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (1, -1), (-1, 1), (1, 1)]

        open_heap = []
        # 将起始点加入开放堆
        heappush(open_heap, (0, start))
        # 记录路径的前驱节点
        came_from = {}
        # 记录从起始点到各节点的实际代价
        g_score = {start: 0}

        while open_heap:
            # 从开放堆中取出当前代价最小的节点
            current = heappop(open_heap)[1]

            # 如果当前节点是目标节点
            if current == end:
                path = []
                # 重构路径
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                # 返回逆序的路径
                return path[::-1]

            # 遍历所有可能的方向
            for dx, dy in directions:
                # 计算邻居节点的坐标
                neighbor = (current[0] + dx, current[1] + dy)
                # 边界检测
                if not (0 <= neighbor[0] < constant.GRID_WIDTH and
                        0 <= neighbor[1] < constant.GRID_HEIGHT):
                    continue
                # 障碍检测
                if constant.grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                # 计算从当前节点到邻居节点的代价
                tentative_g = g_score[current] + ((dx ** 2 + dy ** 2) ** 0.5)
                # 如果邻居节点未被访问过或新的代价更小
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    # 更新前驱节点
                    came_from[neighbor] = current
                    # 更新实际代价
                    g_score[neighbor] = tentative_g
                    # 计算启发式代价
                    f_score = tentative_g + ((neighbor[0] - end[0]) ** 2 +
                                             (neighbor[1] - end[1]) ** 2) ** 0.5
                    # 将邻居节点加入开放堆
                    heappush(open_heap, (f_score, neighbor))
        # 如果没有找到路径，返回None
        return None  # 无可用路径

    def _check_collision(self, axis, delta, direction):
        """碰撞检测方法"""
        move_success = True
        collided = pygame.sprite.spritecollideany(self, walls)
        # 墙壁碰撞处理
        if collided:
            if axis == 'x':
                if delta > 0:
                    self.rect.right = collided.rect.left
                else:
                    self.rect.left = collided.rect.right
            else:  # y轴
                if delta > 0:
                    self.rect.bottom = collided.rect.top
                else:
                    self.rect.top = collided.rect.bottom
            move_success = False
        # 玩家/敌人碰撞检测
        # 玩家检测敌人，敌人检测玩家
        if "player" in self.label:
            target_group = enemies
        elif "enemy" in self.label:
            target_group = players
        else:
            target_group = pygame.sprite.Group()
        collided = pygame.sprite.spritecollideany(self, target_group)
        if collided:
            if axis == 'x':
                if delta > 0:
                    self.rect.right = collided.rect.left
                else:
                    self.rect.left = collided.rect.right
            else:
                if delta > 0:
                    self.rect.bottom = collided.rect.top
                else:
                    self.rect.top = collided.rect.bottom
            move_success = False
        # 敌人间碰撞检测（非Boss）
        if "enemy" in self.label and "boss" not in self.label:
            enemies_collided = [e for e in pygame.sprite.spritecollide(self, enemies, False) if e != self]
            if enemies_collided:
                collided = enemies_collided[0]
                if axis == 'x':
                    if delta > 0:
                        self.rect.right = collided.rect.left
                    else:
                        self.rect.left = collided.rect.right
                else:
                    if delta > 0:
                        self.rect.bottom = collided.rect.top
                    else:
                        self.rect.top = collided.rect.bottom
                move_success = False
        return move_success

    def move(self, dx_0_1=0.0, dy_0_1=0.0):
        """
        坦克移动方法
        :param dx_0_1: x轴移动方向与速度倍数(-1~1)
        :param dy_0_1: y轴移动方向与速度倍数(-1~1)
        :return: 是否移动成功(遇到障碍物返回False)
        """
        move_success = True
        """坦克移动方向判断"""
        if dx_0_1 < 0:
            self.direction = "left"
        elif dx_0_1 > 0:
            self.direction = "right"
        elif dy_0_1 < 0:
            self.direction = "up"
        elif dy_0_1 > 0:
            self.direction = "down"
        else:
            self.direction = "null"
        self.move_direction_dx = dx_0_1
        self.move_direction_dy = dy_0_1
        # 处理x轴移动
        if dx_0_1 != 0:
            #  当前速度小于1时，特定帧移动1像素
            if self.speed < 1:
                if variable.index % round(1 / self.speed) == 0:
                    self.rect.x += dx_0_1
            else:
                self.rect.x += round(dx_0_1 * self.speed)
            # 处理碰撞
            move_success = self._check_collision('x', dx_0_1, "right" if dx_0_1 > 0 else "left")
        # 处理y轴移动
        if dy_0_1 != 0:
            # 当前速度小于1时，特定帧移动1像素
            if self.speed < 1:
                if variable.index % round(1 / self.speed) == 0:
                    self.rect.y += dy_0_1
            else:
                self.rect.y += round(dy_0_1 * self.speed)
            move_success = self._check_collision('y', dy_0_1, "down" if dy_0_1 > 0 else "up")
        # 确保不超出屏幕边界
        if not constant.screen_rect.colliderect(self.rect):
            move_success = False
        self.rect.clamp_ip(constant.screen_rect)
        # 更新移动状态
        if not move_success:
            self.move_direction_dx = 0
            self.move_direction_dy = 0
        return move_success

    def shoot(self, direction='null', deviation_angle=0, bullet_speed_addition=0):
        """
        射击方法
        :param bullet_speed_addition: 子弹速度
        :param deviation_angle: 子弹偏移角度(用于计算偏移量)
        :param direction: 射击方向(默认使用当前方向)
        """
        if "player" in self.label:
            constant.shooting_sound.play()  # 音效
        # 子弹生成
        if direction == 'null':
            direction = self.direction

        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery,
            direction,
            self.damage,
            label=self.label,
            move_direction_dx_dy=(self.move_direction_dx, self.move_direction_dy),
            tank_speed=self.speed,
            deviation_angle=deviation_angle,
            speed=bullet_speed_addition + self.bullet_speed,
            bullet_range=self.range
        )

        # 散射发射
        if "player" in self.label and "scatterer" in self.card_functions_list:
            bullets_number = self.card_functions_list.count("scatterer") * 4
            for _ in range(bullets_number):
                bullet1 = Bullet(
                    self.rect.centerx,
                    self.rect.centery,
                    direction,
                    self.damage,
                    label=self.label,
                    move_direction_dx_dy=(self.move_direction_dx, self.move_direction_dy),
                    tank_speed=self.speed,
                    deviation_angle=deviation_angle + random.uniform(-45, 45),
                    speed=bullet_speed_addition + self.bullet_speed + random.uniform(1, 4),
                    bullet_range=self.range
                )
                all_sprites.add(bullet1)
                bullets.add(bullet1)
        else:
            # 默认发射
            all_sprites.add(bullet)
            bullets.add(bullet)
        return bullets

    def update(self):
        """坦克更新方法"""
        # 速度
        if self.speed > 10:
            self.speed = 10
        # 伤害
        if self.damage_multiplier <= 0:
            self.damage_multiplier = 0.0001
        if self.critical_chance >= 100:
            critical_chance = 100
        else:
            critical_chance = self.critical_chance
        if random.randint(1, 100) <= critical_chance and 'player' in self.label:  # 暴击
            self.damage = self.critical_damage / 100 * (
                    self.damage_initial * self.damage_multiplier + random.randint(0, self.random_damage_range))  # 随机伤害
        else:
            self.damage = self.damage_initial * self.damage_multiplier + random.randint(0,
                                                                                        self.random_damage_range)  # 随机伤害
        # debug模式2
        if "player" in self.label and 2 in debug_mode:
            self.damage = 99999999999999999999
        # 道具冷却
        if self.is_prop_cooling:
            self.prop_cooling_count += 1
            if self.prop_cooling_count >= self.prop_cooling_max:
                self.is_prop_cooling = False
        else:
            self.prop_cooling_count = self.prop_cooling_max
        # 射速
        if self.shoot_speed >= 3:
            self.shoot_speed = 3
        if self.shoot_speed_multiplier <= 0:
            self.shoot_speed_multiplier = 0.0001
        self.shoot_cooling_count_max = 3 // (self.shoot_speed * self.shoot_speed_multiplier)  # 射击冷却最大值
        # 子弹速度
        player = None
        for _ in players:
            player = _  # 获取玩家对象
        if player.bullet_speed <= 0.1:
            player.bullet_speed = 0.1
        # 生命不超过最大值,不为负数
        if self.health > self.health_max:
            self.health = self.health_max
        if self.health <= 0:
            self.health = 0
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)
        # debug模式1
        if "player" in self.label and self.health <= 0 and 1 in debug_mode:
            self.health = 1
        # 玩家死亡
        if self.health <= 0 and "player" in self.label and variable.game_state == "game_start":
            self.health = 0
            constant.bgm.stop()  # 停止BGM
            constant.game_over_sound.play()  # 游戏结束音效
            variable.game_state = "game_over"
        # 敌人死亡
        global boss1_dead
        if self.health <= 0 and "enemy" in self.label:
            constant.death_sound.play()  # 死亡音效
            if "boss1" in self.label:
                boss1_dead = True
            self.kill()
            # 分数增加
            variable.score += self.score_level

            if player.level <= 150:
                new_enemy_spawn_timer = Timer(3, 'new_enemy_spawn_timer')
                timers.add(new_enemy_spawn_timer)
            else:
                if not boss1_dead and function.count_label_sprites(enemies, 'boss') == 0:
                    boss_spawn_timer = Timer(10, 'boss_spawn_timer')
                    timers.add(boss_spawn_timer)
                elif function.count_label_sprites(enemies, 'boss') == 0:
                    boss_spawn_timer = Timer(10, 'boss_spawn_timer')
                    timers.add(boss_spawn_timer)
        """敌人自动行为更新"""
        if "enemy" in self.label:
            # 计算敌人到玩家的向量
            Dx = player.rect.centerx - self.rect.centerx
            Dy = player.rect.centery - self.rect.centery
            distance = (Dx ** 2 + Dy ** 2) ** 0.5
            # 智能移动决策
            if distance < 400 and "boss" not in self.label:  # 近距离追踪 且 非Boss
                """敌人a*路径规划"""
                # 更新路径
                if distance > 400 and variable.index % 30 == 0:  # 远距离时30帧更新一次
                    self.path = self.find_path(player)
                elif distance <= 400 and variable.index % 10 == 0:  # 近距离时10帧更新一次
                    self.path = self.find_path(player)
                    # 路径跟随
                if self.path:
                    # 获取当前路径的第一个目标点
                    target_grid = self.path[0]
                    # 计算目标点的中心x坐标
                    target_x = target_grid[0] * constant.GRID_SIZE + constant.GRID_SIZE / 2
                    # 计算目标点的中心y坐标
                    target_y = target_grid[1] * constant.GRID_SIZE + constant.GRID_SIZE / 2
                    # 计算目标点与当前敌人位置的x方向距离
                    dx = target_x - self.rect.centerx
                    # 计算目标点与当前敌人位置的y方向距离
                    dy = target_y - self.rect.centery
                    # 计算目标点与当前敌人位置的欧氏距离
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    # 如果距离小于网格大小的一半，表示接近当前目标点
                    if distance < constant.GRID_SIZE / 2:  # 接近当前目标点
                        # 如果路径长度大于1，移除当前目标点
                        if len(self.path) > 1:
                            self.path.pop(0)
                    else:
                        # 计算x方向的移动方向
                        move_x = 1 if dx > 0 else -1 if dx < 0 else 0
                        # 计算y方向的移动方向
                        move_y = 1 if dy > 0 else -1 if dy < 0 else 0
                        # 根据计算的移动方向移动敌人
                        self.move(move_x, move_y)
                else:
                    #  直接移动到玩家
                    if abs(Dx) > abs(Dy):
                        move_x = 1 if Dx > 0 else -1
                        move_success = self.move(move_x, 0)
                        if not move_success:
                            move_y = 1 if Dy > 0 else -1
                            self.move(0, move_y)
                    else:
                        move_y = 1 if Dy > 0 else -1
                        move_success = self.move(0, move_y)
                        if not move_success:
                            move_x = 1 if Dx > 0 else -1
                            self.move(move_x, 0)
                    self.direction = "right" if Dx > 0 else "left" if Dx < 0 else "down" if Dy > 0 else "up"
            else:
                # 随机选择移动方向(遇障碍物回避)
                if random.randint(1, 30) == 1:
                    self.ai_move_direction_stateX = random.choice(["left", "right", "stop"])
                    self.ai_move_direction_stateY = random.choice(["up", "down", "stop"])
                if self.ai_move_direction_stateX == "left":
                    move_success = self.move(-1, 0)
                    if not move_success:
                        self.ai_move_direction_stateX = "right"
                elif self.ai_move_direction_stateX == "right":
                    move_success = self.move(1, 0)
                    if not move_success:
                        self.ai_move_direction_stateX = "left"
                if self.ai_move_direction_stateY == "up":
                    move_success = self.move(0, -1)
                    if not move_success:
                        self.ai_move_direction_stateX = "down"
                elif self.ai_move_direction_stateY == "down":
                    move_success = self.move(0, 1)
                    if not move_success:
                        self.ai_move_direction_stateX = "up"
            # 精准射击逻辑
            if distance < 800 or "boss" in self.label or "sniper" in self.label:  # 仅在有效射程内射击,boss无视射程
                # 根据距离调整射击频率
                shoot_prob = 80 if distance < 400 else 150
                if "boss" in self.label:
                    shoot_prob = 50
                if random.randint(1, shoot_prob) == 1:
                    if "sniper" in self.label:
                        # 定向射击
                        if Dx > 0 and Dy > 0:
                            deviation_angle = round(math.atan2(abs(Dx), abs(Dy)) / math.pi * 180)
                            self.shoot("down", deviation_angle, 0)
                        if Dx < 0 and Dy < 0:
                            deviation_angle = round(math.atan2(abs(Dx), abs(Dy)) / math.pi * 180)
                            self.shoot("up", deviation_angle, 0)
                        if Dx < 0 < Dy:
                            deviation_angle = round(math.atan2(abs(Dy), abs(Dx)) / math.pi * 180)
                            self.shoot("left", deviation_angle, 0)
                        if Dx > 0 > Dy:
                            deviation_angle = round(math.atan2(abs(Dy), abs(Dx)) / math.pi * 180)
                            self.shoot("right", deviation_angle, 0)
                    else:
                        # 精确计算射击方向,boss预测强
                        predict_steps = 4 if "boss" in self.label else 2
                        target_x = player.rect.centerx + player.move_direction_dx * player.speed * predict_steps
                        target_y = player.rect.centery + player.move_direction_dy * player.speed * predict_steps
                        # 计算需要的射击方向
                        predict_dx = target_x - self.rect.centerx
                        predict_dy = target_y - self.rect.centery

                        if abs(predict_dx) > abs(predict_dy):
                            shoot_dir = "right" if predict_dx > 0 else "left"
                        else:
                            shoot_dir = "down" if predict_dy > 0 else "up"
                        self.shoot(shoot_dir)
            # boss1特殊行为
            if "boss1" in self.label:
                self.bullet_speed = 8
                # 八向射击
                if random.randint(1, 100) == 1:
                    self.shoot("up", 0, 3)
                    self.shoot("up", 45)
                    self.shoot("down", 0, 3)
                    self.shoot("down", 45)
                    self.shoot("left", 0, 3)
                    self.shoot("left", 45)
                    self.shoot("right", 0, 3)
                    self.shoot("right", 45)
                # 定向射击
                if distance < 800:
                    self.shoot_cooling_count_max = 3
                else:
                    self.shoot_cooling_count_max = 1
                if self.is_shoot_cooling:
                    self.shoot_cooling_count += 0.1
                    if self.shoot_cooling_count >= self.shoot_cooling_count_max:
                        self.shoot_cooling_count = 0
                        self.is_shoot_cooling = False
                else:
                    self.is_shoot_cooling = True
                    if Dx > 0 and Dy > 0:
                        deviation_angle = round(math.atan2(abs(Dx), abs(Dy)) / math.pi * 180)
                        self.shoot("down", deviation_angle, 2)
                    if Dx < 0 and Dy < 0:
                        deviation_angle = round(math.atan2(abs(Dx), abs(Dy)) / math.pi * 180)
                        self.shoot("up", deviation_angle, 2)
                    if Dx < 0 < Dy:
                        deviation_angle = round(math.atan2(abs(Dy), abs(Dx)) / math.pi * 180)
                        self.shoot("left", deviation_angle, 2)
                    if Dx > 0 > Dy:
                        deviation_angle = round(math.atan2(abs(Dy), abs(Dx)) / math.pi * 180)
                        self.shoot("right", deviation_angle, 2)
