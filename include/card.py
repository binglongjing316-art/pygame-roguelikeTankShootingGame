import copy

from include.sprites_init import players

card_options = []  # 当前可选功能卡列表
selected_card = None  # 玩家选择的卡片
card_functions_all = [  # 所有可能的功能选项
    {"name": "leech+2%", "type": "leech", "value": 0.02, "redrawProb": 30, "level": 1, "ID": 1},
    {"name": "critical chance+5%", "type": "crit_chance", "value": 5, "redrawProb": 0, "level": 0, "ID": 2},
    {"name": "critical damage+15%", "type": "crit_dmg", "value": 15, "redrawProb": 0, "level": 0, "ID": 3},
    {"name": "hp+100", "type": "health", "value": 100, "redrawProb": 0, "level": 0, "ID": 4},
    {"name": "shoot speed+0.1", "type": "shoot_speed", "value": 0.1, "redrawProb": 30, "level": 1, "ID": 5},
    {"name": "speed+10%", "type": "speed", "value": 1.1, "redrawProb": 0, "level": 0, "ID": 6},
    {"name": "bullet speed+0.5", "type": "bullet_speed", "value": 0.5, "redrawProb": 0, "level": 0, "ID": 7},
    {"name": "range+15", "type": "range", "value": 15, "redrawProb": 0, "level": 0, "ID": 8},
    {"name": "range+50", "type": "range", "value": 50, "redrawProb": 50, "level": 2, "ID": 9},
    {"name": "milk(dmg down,shoot speed up)", "type": "function", "value": "milk", "redrawProb": 60, "level": 2,
     "ID": 10},
    {"name": "penetrate(penetrate,range up)", "type": "function", "value": "penetrate", "redrawProb": 80, "level": 3,
     "ID": 11},
    {"name": "borer(dmg down,shoot speed down,frame injury)", "type": "function", "value": "borer",
     "redrawProb": 95, "level": 4, "ID": 12},
    {"name": "dementia(dmg up,range up,bullet speed down)", "type": "function", "value": "dementia",
     "redrawProb": 90, "level": 2, "ID": 13},
    {"name": "scatterer", "type": "function", "value": "scatterer", "redrawProb": 85, "level": 3, "ID": 14},
    {"name": "consciousness(track)", "type": "function", "value": "consciousness", "redrawProb": 95, "level": 4,
     "ID": 15},
    {"name": "boom", "type": "prop", "value": "boom", "redrawProb": 85, "level": 3, "ID": 16},
    {"name": "stone(damage+50%,speed-50%)", "type": "function", "value": "stone", "redrawProb": 70, "level": 2,
     "ID": 17},
    {"name": "damage+20%", "type": "damage_rate", "value": 1.2, "redrawProb": 50, "level": 1, "ID": 18}
]
card_functions = copy.deepcopy(card_functions_all)  # 当前可选功能卡列表


def card_function(function={} or "ID" or ("type", "value")):
    """
    卡片功能函数
    :param function: 卡片功能 可以是字典、ID或(type, value)元组
    :return: 成功返回"success"，失败返回错误信息
    """
    # 选择卡片后
    selected_card_dict = "null"
    if type(function) == dict:
        selected_card_dict = function
    elif type(function) == str:
        try:
            function = int(function)
        except ValueError:
            return "ID must be an integer"
        for f in card_functions_all:
            if f["ID"] == function:
                selected_card_dict = f
        if selected_card_dict == "null":
            return "ID out of range"
    else:
        for f in card_functions_all:
            if f["type"] == function[0] and f["value"] == function[1]:
                selected_card_dict = f
        if selected_card_dict == "null":
            return "function not found"

    # 选择数值卡片后
    player = None
    for player in players:
        pass
    if selected_card_dict["type"] == "leech":
        player.leech_rate += selected_card_dict["value"]
    elif selected_card_dict["type"] == "crit_chance":
        player.critical_chance += selected_card_dict["value"]
    elif selected_card_dict["type"] == "crit_dmg":
        player.critical_damage += selected_card_dict["value"]
    elif selected_card_dict["type"] == "health":
        player.health_max += selected_card_dict["value"]
        player.health += selected_card_dict["value"]
    elif selected_card_dict["type"] == "shoot_speed":
        player.shoot_speed += selected_card_dict["value"]
    elif selected_card_dict["type"] == "speed":
        player.speed *= selected_card_dict["value"]
    elif selected_card_dict["type"] == "bullet_speed":
        player.bullet_speed += selected_card_dict["value"]
    elif selected_card_dict["type"] == "range":
        player.range += selected_card_dict["value"]
    elif selected_card_dict["type"] == "damage":
        player.damage_initial += selected_card_dict["value"]
    elif selected_card_dict["type"] == "damage_rate":
        player.damage_initial *= selected_card_dict["value"]

        # 选择功能卡或道具卡后
    elif selected_card_dict["type"] == "function" or selected_card_dict["type"] == "prop":
        # 默认是一次性卡牌
        card_disposable = True
        if selected_card_dict["type"] == "prop":
            # 移除原有的道具卡
            if len(player.prop_list) >= 1:
                player.prop_list.pop(0)
            # 添加卡牌到玩家道具列表
            player.prop_list.append(selected_card_dict["value"])

        elif selected_card_dict["type"] == "function":
            # 添加卡牌到玩家卡牌列表
            player.card_functions_list.append(selected_card_dict["value"])
        # 功能卡处理（一次性获得时）
        if selected_card_dict["value"] == "milk":
            player.shoot_speed_multiplier *= 2
            player.damage_multiplier *= 0.4
        if selected_card_dict["value"] == "penetrate":
            player.range += 50
        if selected_card_dict["value"] == "borer":
            player.shoot_speed_multiplier *= 0.3
            player.damage_multiplier *= 0.5
        if selected_card_dict["value"] == "dementia":
            player.bullet_speed -= 3
            player.damage_multiplier += 0.4
            player.range += 50
        if selected_card_dict["value"] == "scatterer":
            card_disposable = False
            if "scatterer" in player.card_functions_list:
                pass
            else:
                player.shoot_speed_multiplier *= 0.5
                player.bullet_speed -= 4
        if selected_card_dict["value"] == "consciousness":
            card_disposable = False
        if selected_card_dict["value"] == "stone":
            player.damage_multiplier += 0.5
            player.speed -= player.speed*0.5
        # 道具卡处理（一次性获得时）
        if selected_card_dict["value"] == "boom":
            player.prop_cooling_max = 300
        # 卡牌组删除一次性卡牌
        if selected_card_dict in card_functions and card_disposable:
            for _ in card_functions:
                if _["ID"] == selected_card_dict["ID"]:
                    card_functions.remove(_)

    # 改变某些卡牌概率（每次选卡后）
    for _ in card_functions:
        if _["type"] == "range":
            if player.range >= 300:
                _["redrawProb"] = 100
            elif 200 <= player.range < 300:
                _["redrawProb"] = 90
            elif 100 <= player.range < 200:
                _["redrawProb"] = 80
            if "consciousness" in player.card_functions_list:
                _["redrawProb"] = 50
        if _["value"] == "scatterer":
            if selected_card_dict["value"] == "scatterer":
                _["redrawProb"] += 5
        if _["value"] == "consciousness":
            if selected_card_dict["value"] == "consciousness":
                _["redrawProb"] += 1
    return "success"
